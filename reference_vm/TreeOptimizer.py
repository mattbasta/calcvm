# TreeOptimizer.py, initial code by D. Parson, February 2012,
# for use in CSC 526, Compiler II, Spring 2012.
# Add support for O1 in Spring 2012 assignment 2.

import copy
from TypeChecks import tIsArray

class TreeOptimizer(object):
    '''
    This class rewrites parse trees and abstract syntax trees according
    to optimization levels.
    '''
    def __init__(self, optimizationLevel):
        '''
        Set the optimization level. Valid values are 0 through 2.
        Level 0 just returns the parse tree with no changes.
        Level 1 flattens the argument lists for &&, ||, ~  operators,
        and it minimizes array copy-casting by propagating the assigned
        array type downward as an inherited attribute. Level 1 also moves
        array values consisting solely of constants into static storage.
        Level 2 adds detection of tail calls, denoted in the output tree
        as a tailcall instead of a funcall.
        '''
        self.level = optimizationLevel
    def optimize(self, parsetree, outerSymtab):
        '''
        Write a new abstract syntax tree based on the parsetree parameter
        (which is not mutated) according to the optimizationLevel passed
        to the constructor. An optimizationLevel of 0 returns the input
        parsetree.
        '''
        if (self.level == 0):
            return parsetree
        result = ()
        for statement in parsetree:
            result = result + (TreeOptimizer.visitor[statement[0]](
                self, statement, outerSymtab, {}),)
        return result
    def printexpression(self, subtree, mysymtab, inherited):
        '''
        printexpression copies its subtree. It passes no inherited attributes.
        '''
        return (subtree[0], TreeOptimizer.visitor[subtree[1][0]](
            self, subtree[1], mysymtab, {}))
    def varassign(self, subtree, mysymtab, inherited):
        '''
        varassign copies its subtree. If it is assigning to an array
        variable, it propagates the receiving array type as an inherited
        attribute.
        '''
        attrs = {}
        if tIsArray(subtree[2][1]):
            attrs['arraytype'] = subtree[2][1]
        return (subtree[0], subtree[1], subtree[2],
            TreeOptimizer.visitor[subtree[3][0]](
                self, subtree[3], mysymtab, attrs))
    def funcassign(self, subtree, outersymtab, inherited):
        '''
        funcassign copies its subtree. If it is returning an array value,
        it propagates the return array type as an inherited attribute.
        It also propagates a tailcall attribute for the return expression
        for optimization levels >= 2.
        '''
        # outersymtab is this function's enclosing scope.
        funcname = subtree[1]
        funcentry = outersymtab[funcname]
        innersymtab = funcentry[4]
        statements = ()
        for statementSubtree in subtree[4]:
            statements = statements +                       \
                (TreeOptimizer.visitor[statementSubtree[0]](
                    self, statementSubtree, innersymtab, {}),)
        attrs = {}
        if (self.level > 1):
            # Pass symbol table entry needed later for tail-call-postamble.
            attrs['tailcall'] = (subtree, outersymtab)
        if tIsArray(subtree[2][1]):
            attrs['arraytype'] = subtree[2][1]
        retexpr = ('return',
            TreeOptimizer.visitor[subtree[5][1][0]](
                self, subtree[5][1], innersymtab, attrs))
        return (subtree[0], subtree[1], subtree[2], subtree[3],
            statements, retexpr)
    def binaryOperation(self, subtree, mysymtab, inherited):
        '''
        binaryOperation copies its subtree. Array concatenation passes
        destination array type as an inherited attribute.
        '''
        attrs = self.__purgeAttrs__(['tailcall'], inherited)
        return (subtree[0], subtree[1],
            TreeOptimizer.visitor[subtree[2][0]](   # left subexpression
                self, subtree[2], mysymtab, attrs),
            TreeOptimizer.visitor[subtree[3][0]](   # right subexpression
                self, subtree[3], mysymtab, attrs))
    def logicalOperation1(self, subtree, mysymtab, inherited,
            isRootLogical=True):
        '''
        logicalOperation1 is an O1 tree flattener for && and || and ~.
        It collapses adjacent groups of && operations, or of || operations,
        or ~ (not differents ones at the same time), working left-to-right.
        Implicit left and explicit right association are discarded.
        The resulting flattened subtree evaluates left-to-right.
        It collects adjacent logicals with an inorder walk of the tree.
        It also propagates a tail call to its final boolean when the latter
        is a funcall.
        '''
        flatargs = []
        if subtree[2][0][0] == subtree[0]:
            flatargs += self.logicalOperation1(subtree[2][0], mysymtab, {},
                isRootLogical=False)
        else:
            flatargs.append(TreeOptimizer.visitor[subtree[2][0][0]](
                self, subtree[2][0], mysymtab, {}))
        if subtree[2][1][0] == subtree[0]:
            flatargs += self.logicalOperation1(subtree[2][1], mysymtab, {},
                isRootLogical=False)
        else:
            flatargs.append(TreeOptimizer.visitor[subtree[2][1][0]](
                self, subtree[2][1], mysymtab, {}))
        if isRootLogical:
            if inherited.has_key('tailcall') and flatargs[-1][0] == 'funcall':
                # Redo the tree rewrite now that we know that the rightmost
                # entry is a funcall. It still won't change to a tailcall
                # if the call is to an inner function.
                flatargs[-1] = self.funCall(flatargs[-1], mysymtab, inherited)
            return (subtree[0], subtree[1], tuple(flatargs))
        else:
            return flatargs

    def unaryOperation(self, subtree, mysymtab, inherited):
        '''
        unaryOperation copies its subtree. It passes no inherited attributes.
        '''
        return (subtree[0], subtree[1],
            TreeOptimizer.visitor[subtree[2][0]](   # single subexpression
                self, subtree[2], mysymtab, {}))
    def conditionalOperation(self, subtree, mysymtab, inherited):
        '''
        conditionalOperation copies its subtree.
        It passes tailcall inherited to its result expressions
        '''
        return (subtree[0], subtree[1],
            TreeOptimizer.visitor[subtree[2][0]](   # boolean expression 1
                self, subtree[2], mysymtab, {}),
            TreeOptimizer.visitor[subtree[3][0]](   # the IF expression
                self, subtree[3], mysymtab, inherited),
            TreeOptimizer.visitor[subtree[4][0]](   # the ELSE expression
                self, subtree[4], mysymtab, inherited))
    def idLookup(self, subtree, mysymtab, inherited):
        '''
        idLookup returns its subtree. It passes no inherited attributes.
        '''
        return subtree
    def funCall(self, subtree, mysymtab, inherited):
        '''
        funCall copies its subtree. It propogates an array parameter's
        type to its value expression via an inherited attribute.
        '''
        symbolEntry = mysymtab[subtree[2]]
        outlinks = None
        location = None
        paramlist = None
        if symbolEntry[0] == 'func':
            paramlist = symbolEntry[3]
            isInnerFunction = True
        else:           # symbolEntry[0] == 'symref':
            isInnerFunction = False
            defsymtab = symbolEntry[3]
            originalEntry = defsymtab[subtree[2]]
            paramlist = originalEntry[3]
        argtree = ()
        paramix = 0
        for arg in subtree[3]:
            attrs = {}
            if tIsArray(paramlist[paramix][1]):
                attrs['arraytype'] = paramlist[paramix][1]
            argtree = argtree + (TreeOptimizer.visitor[arg[0]](
                self, arg, mysymtab, attrs),)
            paramix += 1
        # We cannot do a tail call on an inner function because we need to
        # keep the static activation context intact.
        if inherited.has_key('tailcall') and not isInnerFunction:
            return ('tailcall', subtree[1], subtree[2], argtree,
                inherited['tailcall'])
        else:
            return (subtree[0], subtree[1], subtree[2], argtree)
    def constantCopy(self, subtree, mysymtab, inherited):
        '''
        constantCopy copies its subtree. It passes no inherited attributes.
        '''
        return subtree
    def typeCast(self, subtree, mysymtab, inherited):
        '''
        typeCast copies its subtree. It passes no inherited attributes.
        '''
        return (subtree[0], subtree[1],
            TreeOptimizer.visitor[subtree[2][0]](
                self, subtree[2], mysymtab, {}))
    def arrayValues(self, subtree, mysymtab, inherited):
        '''
        arrayValues copies its subtree. If all initialization values are
        constants (a synthesized attribute), then it changes root tag
        'arrayvalues' to 'arrayliterals' to support allocation in static
        storage. Also it propagates inherited result type downward
        when assigning into variables, parameters and return values.
        '''
        scalars = ()
        if (inherited.has_key('arraytype')):
            arraytype = inherited['arraytype']
        else:
            arraytype = subtree[1]
        if len(subtree[2]) == 0:
            rootname = 'arrayvalues'
        elif self.level >= 1:
            rootname = 'arrayliterals'
        else:
            rootname = 'arrayvalues'
        for subexpr in subtree[2]:
            scalars = scalars + (TreeOptimizer.visitor[subexpr[0]](
                self, subexpr, mysymtab, {}),)
            if subexpr[0] != 'constant':
                rootname = 'arrayvalues'
        return (rootname, arraytype, scalars)
    def arrayLength(self, subtree, mysymtab, inherited):
        '''
        arrayLength copies its subtree. It passes no inherited attributes.
        '''
        return subtree
    # mapping from parse tree and abstract syntax tree symbols at all possible
    # roots of a sub-tree to the tree-visiting method that rewrites it.
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
            r'&&'                   :   logicalOperation1,
            r'||'                   :   logicalOperation1,
            r'~'                    :   logicalOperation1,
            r'uminus'               :   unaryOperation,
            r'unot'                 :   unaryOperation,
            r'?:'                   :   conditionalOperation,
            r'id'                   :   idLookup,
            r'funcall'              :   funCall,
            r'constant'             :   constantCopy,
            r'typecast'             :   typeCast,
            r'arrayvalues'          :   arrayValues,
            r'arraylen'             :   arrayLength
        }

    def __purgeAttrs__(self, attrNames, attrDict):
        newDict = copy.copy(attrDict);
        for aname in attrNames:
            if newDict.has_key(aname):
                del(newDict[aname])
        return newDict
