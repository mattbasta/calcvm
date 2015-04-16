# CodeGenerator.py, initial code by D. Parson, January 2012,
# for use in CSC 526, Compiler II, Spring 2012.
# STUDENT add support for vectors in Spring 2012 assignment 1.

from TypeChecks import tcompat, tIsArray, tBaseType
from vm_in_python.vm import DirectThreadedVM as DTVM
from sys import maxint


DirectThreadedVM = DTVM()


class CodeGenerator(object):
    '''
    This class provides the code generator for the compiler of progcalc.py.
    '''
    def generate(self, parsetree, outerSymtab, outerCodeArray, vmStaticData):
        '''
        Generate all the code of this program by calling other helper
        methods to traverse the parse tree, using helper methods as
        subtree visitors. The parameters are as follows:
        0. self is this object;
        1. parsetree is the top-level parse tree, consisting of
        a sequence of target program statements;
        2. outerSymtab is the symbol table of the outermost scope;
        3. outerCodeArray is the Python list into which to compile
        code for the outermost scope, outside of any function definition.
        '''
        for statement in parsetree:
            CodeGenerator.visitor[statement[0]](
                self, statement, outerSymtab, outerCodeArray, vmStaticData)

    def printexpression(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to print the result of expression
        evaluation residing atop the data stack.
        '''
        # Evaluating an expression without assigning its result (on top of the
        # data_stack) to a variable or parameter means: Print it, followed by
        # a carriage return - line feed.
        # subtree[1][0] gives the category of expression.
        CodeGenerator.visitor[subtree[1][0]](
            self, subtree[1], mysymtab, myvmCode, vmStaticData)
        myvmCode.append(DirectThreadedVM.STEP_PRINT)
        myvmCode.append(DirectThreadedVM.STEP_CRLF)
    def varassign(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to assign the result of expression
        evaluation residing atop the data stack into a new variable at
        the current scope, with possible type conversion necessary,
        e.g. storing a float into an int variable.
        '''
        # If no preceding code leaves any spare values sitting on the
        # data stack (and preceding code should NOT leave unused results of
        # expressions sitting on the data stack), then the result of the above
        # expression is sitting at just the correct offset from FP, i.e.,
        # 'numlocals' offset. In that case no code need be generated here.
        # HOWEVER, if the ID's type is a float and the expression's is an int,
        # or vice versa, we still need to generate STEP_CAST_DOUBLE or
        # STEP_CAST_LONG.
        CodeGenerator.visitor[subtree[3][0]](
            self, subtree[3], mysymtab, myvmCode, vmStaticData)
        vartype = subtree[2][1]
        valuetype = subtree[3][1]
        # TODO: Deal with array[] type implicit casting on variable assignment.
        # In the case where array types match,
        # it is not necessary to adjust reference counts because,
        # when the expression on the data stack loses the array
        # reference, the variable gains it, for a net change of 0.
        if (vartype != valuetype):
            if tIsArray(vartype):
                # Generate code to duplicate the array whose address is
                # on top of the data stack with an array of the correct type
                # via op codes including STEP_ARRAYCPY. *After* this is done,
                # it is necessary to decrement the reference count of the
                # original array via STEP_REFCNT, because popping it off of
                # the data stack is a lost reference. In the end the
                # address of the new array replaces the original on the
                # data stack.
                # My advice is to create a private helper method that
                # generates code for an array "type-casting copy constructor"
                # that you can use here as well as in funcassign() and
                # funCall(). My solution makes a single-line call in each
                # of these three places to my helper method.
                self.__helpTypeCastArray__(myvmCode, vartype)
            elif (vartype == 'int'):
                myvmCode.append(DirectThreadedVM.STEP_CAST_LONG)
            elif (vartype == 'float'):
                myvmCode.append(DirectThreadedVM.STEP_CAST_DOUBLE)
    def __helpTypeCastArray__(self, myvmCode, desttype):
        basetype = tBaseType(desttype)
        if basetype == 'float':
            castarg = 1
        elif basetype == 'int':
            castarg = -1
        else:
            castarg = 0         # should not happen
        # STACK: FROMADDR
        myvmCode.append(DirectThreadedVM.STEP_DUP)
        # FROMADDR FROMADDR
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(castarg)
        # FROMADDR FROMADDR castarg
        myvmCode.append(DirectThreadedVM.STEP_ARRAYCPY)
        # FROMADDR TOADDR
        myvmCode.append(DirectThreadedVM.STEP_SWAP)
        # TOADDR FROMADDR
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(-1)
        # TOADDR FROMADDR -1
        myvmCode.append(DirectThreadedVM.STEP_REFCNT)
        # TOADDR refcnt
        #myvmCode.append(DirectThreadedVM.STEP_DROP)
        # TOADDR
    def funcassign(self, subtree, outersymtab, myvmCode, vmStaticData,
            isHelpingTailcall=False):
        '''
        postorder code generator to compile a function body.
        This method compiles the statement list and the RETURN
        expression code via their subtrees, and then generates code
        for the postamble. Parameter isHelpingTailcall when True
        (NOT the default) generates only cleanup of the stack frame
        for tailcall.
        '''
        # outersymtab is this function's enclosing scope.
        funcname = subtree[1]
        funcentry = outersymtab[funcname]
        functype = funcentry[2]
        paramlist = funcentry[3]
        innersymtab = funcentry[4]
        innercode = funcentry[5]
        if not isHelpingTailcall:
            for statementSubtree in subtree[4]:
                CodeGenerator.visitor[statementSubtree[0]](self,
                    statementSubtree, innersymtab, innercode, vmStaticData)
            CodeGenerator.visitor[subtree[5][1][0]](    # RETURN expression
                self, subtree[5][1], innersymtab, innercode, vmStaticData)
            if (functype != subtree[5][1][1]):  # latter is expression type
                if tIsArray(functype):
                    # Deal with array[] type implicit casting on return
                    # expression.
                    # See comments regarding a helper method for
                    # "type-casting copy constructor" arrays of mismatched types
                    # in varassign().
                    self.__helpTypeCastArray__(innercode, functype)
                else:
                    innercode.append(
                        DirectThreadedVM.STEP_CAST_LONG if functype == 'int'    \
                            else DirectThreadedVM.STEP_CAST_DOUBLE)
            innercode.append(DirectThreadedVM.STEP_CONST)
            innercode.append(0)      # address 0 in the data dictionary
            innercode.append(DirectThreadedVM.STEP_STORE)
        mylocals = innersymtab['#locals']
        myparams = innersymtab['#params']
        # For every local variable and parameter that is an
        # array, decrement its reference count in the process of
        # dropping it from the data stack. Integrate your code below.
        # Make sure to use innersymtab if you need to look up the local
        # variables, and paramlist (extracted from outersymtab) for params.
        # Note that local variables and arguements are popped in the
        # opposite order from which they were pushed. If there are three
        # local variables at offsets [2], [1] and 0 on the stack, [2] pops
        # first. If there were two arguments below [-1] (which holds the
        # static link), [-2] pops before [-3]. innersymtab holds type and
        # stack offset data for locals, and paramlist holds it for parameters.
        for entry in innersymtab.values():
            if (isinstance(entry, tuple) or isinstance(entry, list))    \
                    and entry[0] == 'var' and tIsArray(entry[2]):
                # Allowing entry[3] < 0 does the job for arguments.
                innercode.append(DirectThreadedVM.STEP_FETCH_REGISTER)
                innercode.append(entry[3])
                innercode.append(DirectThreadedVM.STEP_CONST)
                innercode.append(-1)
                innercode.append(DirectThreadedVM.STEP_REFCNT)
                # Made unnecessary by the new VM
                #innercode.append(DirectThreadedVM.STEP_DROP)
        # Now nuke the activation frame.
        innercode.append(DirectThreadedVM.STEP_CONST)
        innercode.append(- (myparams + 1))      # lowest param
        innercode.append(DirectThreadedVM.STEP_CONST)
        innercode.append(mylocals - 1)          # highest local var
        innercode.append(DirectThreadedVM.STEP_DROPFRAME)
        if not isHelpingTailcall:
            innercode.append(DirectThreadedVM.STEP_CONST)
            innercode.append(0)      # address 0 in the data dictionary
            innercode.append(DirectThreadedVM.STEP_FETCH)
            innercode.append(DirectThreadedVM.STEP_RETURN)
    def binaryOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to generate a binary operation
        combining two subexpressions. Enhanced February 2012 to implement
        '+' for two arrays by constructing their concatenation.
        Concatenating a 0-length any[] can actually just use the
        other array without growing a new one, because these arrays
        are immuable.
        '''
        CodeGenerator.visitor[subtree[2][0]](   # left subexpression
            self, subtree[2], mysymtab, myvmCode, vmStaticData)
        CodeGenerator.visitor[subtree[3][0]](   # right subexpression
            self, subtree[3], mysymtab, myvmCode, vmStaticData)
        if tIsArray(subtree[1]):        # Type of sum is an array
            # This should be concatenation of two arrays, make sure:
            if (subtree[0] != '+'):
                raise ValueError, (                                 \
                    "INTERNAL ERROR: Bad op for an array in parse tree: " \
                        + str(subtree[0]))
            # Generate code to set up the data stack for an invocation of
            # STEP_ARRAYCAT, setting its TYPEFLAG to a per-element typecast
            # only if one of the two input arrays has a type mismatch with
            # the destination array.
            # After STEP_ARRAYCAT has completed your generated code must
            # decrement the reference counts for the two original arrays
            # via STEP_REFCNT, and discard everything on the data stack
            # except the new, concatenated array. You do not need to
            # increment its reference count.
            # STACK: LARRAY RARRAY
            castflag = 0
            if (subtree[2][1] != subtree[1] or subtree[3][1] != subtree[1]):
                basetype = tBaseType(subtree[1])
                if (basetype == 'float'):
                    castflag = 1
                elif (basetype == 'int'):
                    castflag = -1
            myvmCode.append(DirectThreadedVM.STEP_OVER)
            myvmCode.append(DirectThreadedVM.STEP_OVER)
            # LARRAY RARRAY LARRAY RARRAY
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(castflag)
            # LARRAY RARRAY LARRAY RARRAY castflag
            myvmCode.append(DirectThreadedVM.STEP_ARRAYCAT)
            # LARRAY RARRAY NEWARRAY
            myvmCode.append(DirectThreadedVM.STEP_SWAP2)
            # NEWARRAY RARRAY LARRAY
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(-1)
            myvmCode.append(DirectThreadedVM.STEP_REFCNT)
            #myvmCode.append(DirectThreadedVM.STEP_DROP)
            # NEWARRAY RARRAY
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(-1)
            myvmCode.append(DirectThreadedVM.STEP_REFCNT)
            #myvmCode.append(DirectThreadedVM.STEP_DROP)
            # NEWARRAY
        else:
            # The results of both expressions are sitting at the top of the data
            # stack, so just generate the appropriate op code.
            operator = subtree[0]

            ltype, rtype = subtree[2][1], subtree[3][1]
            if ltype != rtype:
                cast_types = {"float": DirectThreadedVM.STEP_CAST_DOUBLE,
                              "int": DirectThreadedVM.STEP_CAST_LONG}
                if ltype == "float":
                    myvmCode.append(cast_types[ltype])
                elif rtype == "float":
                    ltype = "float"
                    myvmCode.append(DirectThreadedVM.STEP_SWAP)
                    myvmCode.append(DirectThreadedVM.STEP_CAST_DOUBLE)
                    myvmCode.append(DirectThreadedVM.STEP_SWAP)
                else:
                    raise "Incompatible type casting."

            ltype = {"float": "D", "int": "L", "string": "S"}[ltype]
            operations = {"+": "STEP_%sADD",
                          "-": "STEP_%sSUB",
                          "*": "STEP_%sMULT",
                          "/": "STEP_%sDIV",
                          "%": "STEP_%sMOD",
                          "<": "STEP_%sLT",
                          ">": "STEP_%sGT",
                          "<=": "STEP_%sLE",
                          ">=": "STEP_%sGE",
                          "==": "STEP_%sEQ",
                          "!=": "STEP_%sNEQ"}
            myvmCode.append("StepOpCode %s" % operations[operator] % ltype)
    def logicalOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        inorder code generator to generate short-circuited logical and OR or.
        STUDENT LOGICAL NEEDS TO DEAL WITH > 2 ARGS IN subtree[2]
        STUDENTS: Modify this function accordingly.
        '''
        # PARSON'S SOLUTION
        jmpPoints = []
        finalexpr = len(subtree[2]) - 1
        for i in range(0, len(subtree[2])):
            CodeGenerator.visitor[subtree[2][i][0]](   # next subexpression
                self, subtree[2][i], mysymtab, myvmCode, vmStaticData)

            # Force cast to long
            if subtree[2][i][1] != "int":
                myvmCode.append(DirectThreadedVM.STEP_CAST_LONG)

            if (i < finalexpr):
                myvmCode.append(DirectThreadedVM.STEP_DUP)
                # Leave left expression result on stack if jump is taken.
                if subtree[0] == r'||':     # logical or
                    myvmCode.append(DirectThreadedVM.STEP_LZEQ)
                    # Invert before test.
                myvmCode.append(DirectThreadedVM.STEP_GOTO0)
                jumpoffset = len(myvmCode)    # offset of in-line jump address
                jmpPoints.append(jumpoffset)
                myvmCode.append(None)   # This will get backpatched.
                myvmCode.append(DirectThreadedVM.STEP_DROP)
                # Discard the DUP'd value.
        for jumpoffset in jmpPoints:
            myvmCode[jumpoffset] = ((len(myvmCode)-jumpoffset),)
            # Backpatch later
    def tildeOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        inorder code generator to print and discard left subexpression.
        STUDENT TILDE NEEDS TO DEAL WITH > 2 ARGS IN subtree[2]
        STUDENTS: Modify this function accordingly.
        '''
        # PARSON'S SOLUTION
        finalexpr = len(subtree[2]) - 1
        for i in range(0, len(subtree[2])):
            CodeGenerator.visitor[subtree[2][i][0]](   # next subexpression
                self, subtree[2][i], mysymtab, myvmCode, vmStaticData)
            if (i < finalexpr):
                myvmCode.append(DirectThreadedVM.STEP_PRINT)
                myvmCode.append(DirectThreadedVM.STEP_CRLF)
    def uminusOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to invert a numeric value
        '''
        CodeGenerator.visitor[subtree[2][0]](   # single subexpression
            self, subtree[2], mysymtab, myvmCode, vmStaticData)
        if subtree[2][1] == "int":
            myvmCode.append(DirectThreadedVM.STEP_LMINUS)
        elif subtree[2][1] == "float":
            myvmCode.append(DirectThreadedVM.STEP_DMINUS)
        else:
            raise "Invalid use of unary minus"
    def unotOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to negate a logical (int) value
        '''
        CodeGenerator.visitor[subtree[2][0]](   # single subexpression
            self, subtree[2], mysymtab, myvmCode, vmStaticData)
        if subtree[2][1] == "int":
            myvmCode.append(DirectThreadedVM.STEP_LZEQ)
        elif subtree[2][1] == "float":
            myvmCode.append(DirectThreadedVM.STEP_DZEQ)
        else:
            raise "Invalid use of logical not"
    def conditionalOperation(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        inorder code generator to generate short-circuited ?: operation
        '''
        CodeGenerator.visitor[subtree[2][0]](   # boolean expression 1
            self, subtree[2], mysymtab, myvmCode, vmStaticData)
        myvmCode.append(DirectThreadedVM.STEP_GOTO0)    # jump to else part
        jumpoffset1 = len(myvmCode)
        myvmCode.append(None)
        CodeGenerator.visitor[subtree[3][0]](   # the IF expression
            self, subtree[3], mysymtab, myvmCode, vmStaticData)
        myvmCode.append(DirectThreadedVM.STEP_GOTO) # Past the ELSE code
        jumpoffset2 = len(myvmCode)
        myvmCode.append(None)
        CodeGenerator.visitor[subtree[4][0]](   # the ELSE expression
            self, subtree[4], mysymtab, myvmCode, vmStaticData)
        # Backpatch with relative jump addresses that the linker will resolve.
        myvmCode[jumpoffset1] = ((jumpoffset2 - jumpoffset1 + 1),)
        myvmCode[jumpoffset2] = ((len(myvmCode) - jumpoffset2),)
    def idLookup(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder generator to walk out N static links and fetch this
        variable from its stack frame.
        '''
        symbolEntry = mysymtab[subtree[2]]
        # The parser guarantees that this is a variable lookup.
        outlinks = None
        location = None
        if symbolEntry[0] == 'var':
            outlinks = 0
            location = symbolEntry[3]
        else:           # symbolEntry[0] == 'symref':
            outlinks = symbolEntry[2]
            defsymtab = symbolEntry[3]
            originalEntry = defsymtab[subtree[2]]
            location = originalEntry[3]
        # Subscripting for array names added CSC 526 assn 1 Feb 2012
        subscriptSubtree = None if (len(subtree) == 3) else subtree[3]
        if outlinks > 0:
            myvmCode.append(DirectThreadedVM.STEP_PUSH_FP) # initial static link
            for i in range(0,outlinks):
                myvmCode.append(DirectThreadedVM.STEP_CONST)
                myvmCode.append(-1)
                myvmCode.append(DirectThreadedVM.STEP_LADD)  # add -1 to current FP
                myvmCode.append(DirectThreadedVM.STEP_FETCH_STACK) # fetch outer FP
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(location)
            myvmCode.append(DirectThreadedVM.STEP_LADD)  # variable's address
            myvmCode.append(DirectThreadedVM.STEP_FETCH_STACK) # variable's value
        else:
            myvmCode.append(DirectThreadedVM.STEP_FETCH_REGISTER) # variable's value
            myvmCode.append(location)

        # Increase the refcount if this value is
        # an array, UNLESS (subscriptSubtree != None).
        # After this code is done, the array address must still be
        # on the stack, with nothing else on the stack added by this code.
        # HOWEVER, if (subscriptSubtree != None), then instead of incrementing
        # the refcount, generate code to get the subscript value onto the
        # stack, then code to fetch the element indexed by subscriptSubtree,
        # replacing the array address with the fetched element.
        # subscriptSubtree entails recursive code generation via visitor[].
        if subscriptSubtree != None:
            CodeGenerator.visitor[subscriptSubtree[0]](
                self, subscriptSubtree, mysymtab, myvmCode, vmStaticData)
            myvmCode.append(DirectThreadedVM.STEP_PADD)
            myvmCode.append(DirectThreadedVM.STEP_FETCH)
        elif tIsArray(subtree[1]):
            myvmCode.append(DirectThreadedVM.STEP_DUP)
            # ARRAY ARRAY
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(1)
            myvmCode.append(DirectThreadedVM.STEP_REFCNT)
            # ARRAY refcnt
            #myvmCode.append(DirectThreadedVM.STEP_DROP)
            # ARRAY
    def tailCall(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        Generate a tail call to the current or other function when the
        call is the last step before returning, and the called function
        returns the value that is, in turn, returned by the calling
        function. A tail call does not generate a function call, it
        generates a STEP_GOTO to the start of the called function, using
        the following general steps.
        1. It computes the outgoing arguments for the pseudo-function call.
           Computing arguments must be done before step 2, because
           if an incoming array parameter is also among the outgoing
           argument dependencies, its reference count must not drop to 0
           prematurely.
        2. Conceptually, it removes local variables and parameters,
           decrementing array reference counts as for a normal function
           return's postamble.
        3. It rerranges the data stack to reflect the dropping of all local
           variables, static link and arguments to the current function,
           then it pushes the argument values and static link to the called
           function, then generates a STEP_GOTO to the "called" function.
        Turning tail calls into loops reduces the likelihood of a stack
        overflow at run time. However, with all of the stack manipulation
        overhead for the Step VM, a tail call may run slower than a
        regular function call. Consult the new STEP_DROPFRAME op code as
        a possible time saver for the postamble.
        '''
        # STUDENTS -- delete the next line, then write your code.
        # NOTE that subtree[4] for a 'tailcall' holds the
        # (subtree, outersymboltable) pair for the context of the funcassign
        # for the definition of the function making the tail call.
        # You need that data so you can implement the postamble for
        # the correct parameters and local variables.
        # table entry for the function that is "making the tail call."
        location, numargs = self.funCall(subtree, mysymtab, myvmCode,
            vmStaticData, isRealFunction=False)
        # Arguments are pushed, now do the postamble call.
        self.funcassign(subtree[4][0],subtree[4][1], myvmCode, vmStaticData,
            isHelpingTailcall=True)
        myvmCode.append(DirectThreadedVM.STEP_GOTO)
        myvmCode.append(location)
    def funCall(self, subtree, mysymtab, myvmCode, vmStaticData,
            isRealFunction=True):
        '''
        postorder generator to walk out N static links and invoke this
        function with its correct nesting run-time static scope.
        isRealFunction if False (NOT the default) generates parameters and the
        static link, but not a function call. That is used as a helper by
        tailCall. Returns (functionAddress, numArgsPushed) as required
        by tailcall, where functionAddress is the location of the function
        to call, and numArgsPushed includes the static link.
        '''
        symbolEntry = mysymtab[subtree[2]]
        # The parser guarantees that this is a variable lookup.
        outlinks = None
        location = None
        paramlist = None
        if symbolEntry[0] == 'func':
            outlinks = 0
            location = symbolEntry          # linker backpatches this
            paramlist = symbolEntry[3]
        else:           # symbolEntry[0] == 'symref':
            outlinks = symbolEntry[2]
            defsymtab = symbolEntry[3]
            originalEntry = defsymtab[subtree[2]]
            location = originalEntry
            paramlist = originalEntry[3]
        arglist = subtree[3]
        numArgsPushed = len(arglist) + 1
        offset = len(paramlist) - 1
        for i in range(0, len(paramlist)):
            paramtype = paramlist[i][1][1]
            argument = arglist[i]
            argtype = argument[1]
            CodeGenerator.visitor[argument[0]](
                self, argument, mysymtab, myvmCode, vmStaticData)
            # Enhancement from Fall 2011 assignment 5: Do the type check
            # immediately after expression evaluation.
            if (paramtype != argtype):
                if tIsArray(paramtype):
                    # See comments regarding a helper method for
                    # "type-casting copy constructor" arrays of mismatched
                    # types in varassign().
                    self.__helpTypeCastArray__(myvmCode, paramtype)
                elif paramtype == 'int':
                    myvmCode.append(DirectThreadedVM.STEP_CAST_LONG)
                elif paramtype == 'float':
                    myvmCode.append(DirectThreadedVM.STEP_CAST_DOUBLE)
                else:
                    msg = "INTERNAL ERROR: Illegal implicit type cast to "  \
                        + str(paramtype) + " at call to function "          \
                        + subtree[2] + ", parameter " + paramlist[i][0]
                    raise ValueError, msg
            offset -= 1

        myvmCode.append(DirectThreadedVM.STEP_PUSH_FP) # initial static link
        for i in range(0,outlinks):
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(-1)
            myvmCode.append(DirectThreadedVM.STEP_LADD)  # add -1 to current FP
            myvmCode.append(DirectThreadedVM.STEP_FETCH_STACK) # fetch outer FP
        if (isRealFunction):
            myvmCode.append(DirectThreadedVM.STEP_CALL_SECONDARY)
            # ID's symbol table list for later linking:
            # print "DEBUG FUNCALL OFFSET", len(myvmCode), "OPERAND", location
            myvmCode.append(location)
        return ((location, numArgsPushed))
    def constantPush(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to push a typed constant to the data stack.
        '''
        ctype = subtree[1]
        lexeme = subtree[2]
        inlineData = None
        if ctype == 'string':
            inlineData = lexeme
        elif ctype == 'int':
            inlineData = int(lexeme)
        else:
            inlineData = float(lexeme)
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(inlineData)
    def typeCast(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator to convert the type of the value on
        the data stack to an int, float or string.
        '''
        CodeGenerator.visitor[subtree[2][0]](       # evaluate the expression
            self, subtree[2], mysymtab, myvmCode, vmStaticData)
        if subtree[1] == 'int':
             myvmCode.append(DirectThreadedVM.STEP_CAST_LONG)
        elif subtree[1] == 'float':
             myvmCode.append(DirectThreadedVM.STEP_CAST_DOUBLE)
        elif subtree[1] == 'string':
             myvmCode.append(DirectThreadedVM.STEP_CAST_STRING)
        else:
            raise ValueError, ("INTERNAL ERROR: Bad type cast in parse tree: " \
                + str(subtree[1]))
    def arrayValues(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        inorder code generator to allocate and store an array value
        consisting of 0 or moretype-compatible elements, where a float
        array may contain some integer elements that require type
        conversion, and the base type may be 'any' for an empty array.
        The array value is a nonnegative offset into the data dictionary
        returned by op code STEP_ALLOC.
        '''
        # The parse tree has a list of expressions. You do not need to
        # generate a loop in VM code; you need to write a loop here that
        # iterates over all the expressions in that list. Roughly:
        # 1. Allocate an array with the correct element count via STEP_ALLOC.
        # 2. For each element in the parse tree's list of expressions:
        # 2a. Visit that subtree recursively, generating code to place its
        #     value onto the data stack.
        # 2b. If the type of the generated element does not match the type of
        #     the new array, generate a typecast op code. You can get this
        #     info from the parse tree.
        # 2c. Generate code to store the evaluated element in the new array.
        # 3. Leave only the address of the new array on the data stack. Its
        #    reference count is already correctly set to 1 by STEP_ALLOC.
        # NOTE that STEP_ALLOC for a length of 0 works correctly -- the VM
        # creates a singleton, interned memory region for all 0-element
        # arrays when it starts up. These are intrinsically of type any[].
        # STUDENT #2 REPLACE DYNAMIC ALLOCATION OF ARRAY LITERALS ON THE STACK
        # WITH STATIC ALLOCATION in vmStaticData, which is the static
        # storage class data loaded into data_dictionary at VM load time.
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(len(subtree[2]))
        myvmCode.append(DirectThreadedVM.STEP_ALLOC)
        # STACK: NEWARRAY
        typecast = None
        basetype = tBaseType(subtree[1])
        if basetype == 'float':
            typecast = DirectThreadedVM.STEP_CAST_DOUBLE
        elif basetype == 'int':
            typecast = DirectThreadedVM.STEP_CAST_LONG
        index = 0
        for subexpr in subtree[2]:
            CodeGenerator.visitor[subexpr[0]](  # evaluate the expression
                self, subexpr, mysymtab, myvmCode, vmStaticData)
            if subexpr[1] != basetype and typecast != None:
                myvmCode.append(typecast)
            # NEWARRAY ELEVALUE
            myvmCode.append(DirectThreadedVM.STEP_OVER)
            # NEWARRAY ELEVALUE NEWARRAY
            myvmCode.append(DirectThreadedVM.STEP_CONST)
            myvmCode.append(index)
            myvmCode.append(DirectThreadedVM.STEP_PADD)
            # NEWARRAY ELEVALUE NEWARRAY+IX
            myvmCode.append(DirectThreadedVM.STEP_STORE)
            # NEWARRAY
            index += 1
    def arrayLiterals(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        inorder code generator to allocate and store an array value
        consisting of 0 or more type-compatible CONSTANT elements
        into static storage, with a reference count of maxint.
        '''
        typecast = None
        basetype = tBaseType(subtree[1])
        if basetype == 'float':
            typecast = float
        elif basetype == 'int':
            typecast = int
        elemcount = len(subtree[2])
        regionsize = elemcount + DirectThreadedVM.__MEMOVH__
        region = [regionsize, maxint, elemcount]
        for subexpr in subtree[2]:
            if (typecast):
                region.append(typecast(subexpr[2]))
            else:
                region.append(subexpr[2])
        region.append(regionsize)
        location = len(vmStaticData)
        vmStaticData.extend(region)
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(location + DirectThreadedVM.__MEMAPD__)
    def arrayLength(self, subtree, mysymtab, myvmCode, vmStaticData):
        '''
        postorder code generator leave the length an an array ID
        on top of the data stack.
        '''
        # TODO -- See offsets __MEMLEN__ and __MEMAPD__ in vm.py.
        # Parson used a called to idLookup() as a helper method here.
        # What we have in subtree is for example:
        # ('arraylen', 'int', 'iarray', 'int[]')
        self.idLookup(('id', subtree[3], subtree[2]), mysymtab, myvmCode,
            vmStaticData)
        # STACK: ARRAY

        # Drop the refcnt
        myvmCode.append(DirectThreadedVM.STEP_DUP)
        # ARRAY ARRAY
        myvmCode.append(DirectThreadedVM.STEP_CONST)
        myvmCode.append(-1)
        # ARRAY ARRAY -1
        myvmCode.append(DirectThreadedVM.STEP_REFCNT)
        # ARRAY

        # Get the length
        myvmCode.append(DirectThreadedVM.STEP_ARRAYCOUNT)
        # LENGTH

        # STACK: ARRAY ARRAY
        #myvmCode.append(DirectThreadedVM.STEP_CONST)
        #myvmCode.append(-1)
        #myvmCode.append(DirectThreadedVM.STEP_LSUB)
        #myvmCode.append(DirectThreadedVM.STEP_FETCH)
        # STACK: ARRAY LEN
        #myvmCode.append(DirectThreadedVM.STEP_SWAP)
        # STACK: LEN ARRAY
        #myvmCode.append(DirectThreadedVM.STEP_CONST)
        #myvmCode.append(-1)
        # LEN ARRAY -1
        #myvmCode.append(DirectThreadedVM.STEP_REFCNT)
        # LEN refcnt
        #myvmCode.append(DirectThreadedVM.STEP_DROP)
        # LEN
    # mapping from parsetree symbols at all possible roots of a sub-parsetree
    # to the tree-visting method that generates its code.
    visitor = {
        r'printexpression'      :   printexpression,
        r'varassign'            :   varassign,
        r'funcassign'           :   funcassign,
        r'+'                    :   binaryOperation,
        r'-'                    :   binaryOperation,
        r'*'                    :   binaryOperation,
        r'/'                    :   binaryOperation,
        r'%'                    :   binaryOperation,
        r'=='                   :   binaryOperation,
        r'!='                   :   binaryOperation,
        r'>'                    :   binaryOperation,
        r'>='                   :   binaryOperation,
        r'<'                    :   binaryOperation,
        r'<='                   :   binaryOperation,
        r'&&'                   :   logicalOperation,
        r'||'                   :   logicalOperation,
        r'~'                    :   tildeOperation,
        r'uminus'               :   uminusOperation,
        r'unot'                 :   unotOperation,
        r'?:'                   :   conditionalOperation,
        r'id'                   :   idLookup,
        r'funcall'              :   funCall,
        r'tailcall'             :   tailCall,
        r'constant'             :   constantPush,
        r'typecast'             :   typeCast,
        r'arrayvalues'          :   arrayValues,
        r'arrayliterals'        :   arrayLiterals,
        r'arraylen'             :   arrayLength
    }
