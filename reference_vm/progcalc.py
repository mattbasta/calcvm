# -----------------------------------------------------------------------------
# progcalc.py   A programmable, function language calculator based on
#               calc.py in the PLY distribution.
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Extended for CSC 425, Compilers I, Dr. D. Parson, Fall 2011
# to add nested functions and blocks within functions to this calculator.
# I wrote the grammar extensions. Students added symbol table
# manipulation and type checking for assignment #4, and generation of
# executable code for a virtual machine for assignment #5.
# My solutions are integrated into this file.
#
# Extended for CSC 526, Compilers II, Dr. D. Parson, Spring 2011,
# to move code generation into helper class CodeGenerator in file
# CodeGenerator.py.
# Dr. Parson had added vector parsing and type checking. Students must
# write code generation in file CodeGenerator.py and the run-time
# storage allocator in file vm_in_python/vm.py.
# -----------------------------------------------------------------------------

import sys
import logging
import copy
import re
from pprint import PrettyPrinter
from TypeChecks import printSymtab
from vm_in_python.vm import DirectThreadedVM
from TypeChecks import tcompat, tIsArray, tBaseType
from CodeGenerator import CodeGenerator
from TreeOptimizer import TreeOptimizer
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Tokens

reserved = {        # Map the reserved lexeme to its TOKEN name.
    'function' :            'FUNCTION',
    'int' :                 'INT',
    'float' :               'FLOAT',
    'string' :              'STRING',
    'return' :              'RETURN',
    'ALEN' :                'ARRAY_LENGTH'
}

tokens = (
    'ID', 'FLOATNUMBER', 'INTNUMBER', 'STRINGCONSTANT',
    'EQ_OP', 'LE_OP', 'GE_OP', 'NE_OP', 'LT_OP', 'GT_OP', 'ASSIGN_OP',
    'LBRACE', 'RBRACE', 'LBRACK', 'RBRACK', 'LPAREN', 'RPAREN', 'SEP',
    'ADD_OP', 'SUBTRACT_OP', 'MULTIPLY_OP', 'DIVIDE_OP', 'MODULO_OP',
    'QUESTION_OP', 'COLON_OP', 'LOGAND_OP', 'LOGOR_OP', 'LOGNOT_OP', 'COMMA',
    'TILDE_OP'
) + tuple(reserved.values())    # append TOKENS for reserved words

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if (reserved.has_key(t.value)):
        t.type = reserved[t.value]
    else:
        t.type = 'ID'
    return t

# More specific patterns like t_FLOATNUMBER must come before their
# less specific conflicting patterns like INTNUMBER.
def t_FLOATNUMBER(t):
    "(\d+\\.\d*)|(\d*\\.\d+)"
    # t.value = float(t.value)
    # Lexeme is a string.
    return t

def t_INTNUMBER(t):
    "\d+"
    # t.value = int(t.value)
    # Lexeme is a string.
    return t

def t_STRINGCONSTANT(t):
    "\\'[^']*\\'"
    t.value = str(t.value)
    return t

# Token patterns from assignment 3. Those that overlap with t_ID
# are handled above, and do not appear in this group.
t_ignore =    ' \t'
                                    # Operator TYPE requirements follow.
                                    # Numeric allows mix of int and float.
# RETURN expression type and its FUNCTION declaration type must be
# both numeric or both strings.
# Function formal parameters and function-call actual parameters must be
# both numeric or both strings, i.e., the args must be compatible with params.
#
t_EQ_OP =                "\\=\\="   # args are both numeric or both strings
t_LE_OP =                "<="       # args are both numeric or both strings
t_GE_OP =                ">="       # args are both numeric or both strings
t_NE_OP =                "!="       # args are both numeric or both strings
t_LT_OP =                "<"        # args are both numeric or both strings
t_GT_OP =                ">"        # args are both numeric or both strings
t_ASSIGN_OP =            "\\="      # lvalue and rvalue numeric or both strings
t_ADD_OP =		         "\\+"      # args are both numeric or both strings
t_SUBTRACT_OP =		     "\\-"      # args are both numeric
t_MULTIPLY_OP =		     "\\*"      # args are both numeric
t_DIVIDE_OP =		     "\\/"      # args are both numeric
t_MODULO_OP =		     "\\%"      # args are both int
t_QUESTION_OP =		     "\\?"      # the test condition must be an int
t_COLON_OP =		     "\\:"      # two expressions must have identical type
t_LOGAND_OP =		     "&&"       # args are both int
t_LOGOR_OP =		     "\\|\\|"   # args are both int
t_LOGNOT_OP =		     "!"        # expression must be type int
t_COMMA =                ","
t_TILDE_OP = "~" # Used like C comma operator, discards left expr's result.
t_LBRACE =               "{"
t_RBRACE =               "}"
t_LBRACK =               "\\["      # Added for language vectors csc526 assn1.
t_RBRACK =               "]"        # Added for language vectors csc526 assn1.
t_LPAREN =               "\\("
t_RPAREN =               "\\)"
t_SEP =                  ";"

__global_line_number__ = 1
# If __global_error__ is not yet set, then upon finding an error,
# set it to one of the following and also set __global_error_string__.
# There errors are built-in Python error types.
#
# SyntaxError           on lexical or syntax error
# TypeError             on type mismatch or missing / extra argument
# NameError             symbol not in scope or redefined at same scope
# ValueError            linker raises this on invalid program memory entry
__global_error__ = None
__global_error_string__ = None

def t_newline(t):
    r'\n+'
    global __global_line_number__
    t.lexer.lineno += t.value.count("\n")
    __global_line_number__ = t.lexer.lineno

def t_error(t):
    global __global_error__
    global __global_error_string__
    print "Illegal character '%s'" % t.value[0], "near line",   \
        __global_line_number__
    t.lexer.skip(1)
    if __global_error__ == None:
        __global_error_string__ =   \
            ("ERROR: Illegal character '%s'" % t.value[0]) + " near line "\
            + str( __global_line_number__)
        __global_error__ = SyntaxError

# Build the lexer
import ply.lex as lex
lex.lex()

# STUDENT User this error reporing function for syntax and semantic errors.
def terror(ex, st, isprint=True): # exception type and string
    global __global_error__
    global __global_error_string__
    if (isprint):
        print st
    if __global_error__ == None:
        __global_error_string__ = st
        __global_error__ = ex

# Parsing rules

# Precedence of "e ? e : e" and "! e" borrowed from ANSI C. D. Parson, 11/2011
# Precedence and semantics of '~' borrowed from C's ',' comma operator.
precedence = (
    ('left', 'TILDE_OP'),
    ('nonassoc', 'ASSIGN_OP'),
    ('right', 'QUESTION_OP', 'COLON_OP'),
    ('left', 'LOGOR_OP'),
    ('left', 'LOGAND_OP'),
    ('nonassoc', 'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP', 'LT_OP', 'GT_OP'),
    ('left','ADD_OP','SUBTRACT_OP'),
    ('left','MULTIPLY_OP','DIVIDE_OP', 'MODULO_OP'),
    ('right','UMINUS', 'LOGNOT_OP')
    )

# STUDENT: Implementation for symbol table and code generation data
# structures follow:

# vmCode holds the VM-machine code contents for the compiled VM program.
# This global vmCode list compiles the in-line executable code (the code
# outside of function bodies) during compilation, and then the __link__
# function links subroutine code and transfers it into vmCode after the end
# of compilation.
vmCode = []
# This compiler generates one data_dictionary location to hold a function
# return value while a function postamble is cleaning up the activation
# frame; all other data live on the run-time data stack.
vmStaticData = [0]
# one location, used to temporarily hold RETURN value.

# STUDENT This dictionary 'symtab' is the global-level symbol table.
# There is a global scope that owns this table.
# Each function nested within a scope defines an additional scope.
# Therefore there is a tree of symbol tables, growing up from this root,
# with a new branch added for each nested scope.
# Any entry in the symtab maps the symbol ID to either:
# 1. a symbolic variable, or:
# 2. a named function's information, or
# 3. a symbol used in this symtab's scope but defined in an outer scope.
#    This group includes using outer variables and calling outer functions.
# 4. Special case #* mappings enumerated below.
#
# 1. A variable map looks like this:
#       ID : ('var', ID, type, frameoffset)
# where ID as a key == ID in the value tuple, and type is one of the types,
# currently 'int' 'float' or 'string'
# frameoffset is added in assn5 for variable's location in its activation frame.
# It is [-2] or less for an incoming parameter; [-1] is reserved for
# the static link, which is the FP (frame pointer) of the lexically
# enclosing function activation frame.
# ADDED FOR CSC526 ASSN 1: type may also be 'int[]' 'float[]' or 'string[]'
# for a vector type, in which case the value stored in a variable is an offset
# into the data dictionary obtained via op code STEP_ALLOC.
#
# 2. A function definition map looks like this:
#       ID : ['func', ID, type, paramlist, nestedsymtab, codeaddress]
# (It's a LIST in assignment 5 so we can mutate codeaddress during __link__.)
# where paramlist is a sequence of (ID, type) pairs for the formal parameters.
# The nestedsymtab is the symbol table for the defined function's scope.
# Function definitions can nest. The VM supports only third class functions.
# 'codeaddress' added assn5 for address of start of function in program memory.
# While code is being compiled this field is used as a reference to a
# temporary array (Python list) in which its function is being compiled.
# I have added a '__link__()' call for post-processing in global function
# 'compile' at the bottom of this module that replaces codeaddress-as-list
# into codeaddress-as-integer-location. See additional comments on
# BACKPATCHING below.
# ADDED FOR CSC526 ASSN 1: type may also be 'int[]' 'float[]' or 'string[]'
# for a vector type, in which case the value returned by the function is an
# offset into the data dictionary obtained via op code STEP_ALLOC.
#
# 3. A symbol defined in an outer scope that is used in this scope looks like:
#       ID : ('symref', ID, linksteps, defsymtab)
# where linksteps is an integer >= 1 that counts how many scopes out to
# the ID's definition scope, and defsymtab is a reference to the symtab
# at that scope (that contains the actual definition of ID). Keeping
# track of references defined in outer scopes is useful in avoiding a
# redefinition of a symbol after it has already been used from an outer
# scope (the 'ambiguous symbol' error), and it is useful in code
# generation for keeping track of symbolic links.
# ADDED FOR ASSIGNMENT 5:
# symtab for each scope holds the following counters:
#       '#params' : numberOfParameters for this function, 0 for outer scope
#       '#depth'  : inner scope depth of this function, 0 for outer scope
#       '#locals' : numberOfLocalVariables defined at this scope level
#       '#funcs'  : numberOfNestedFunctions defined at this scope level
# symtab for each scope holds the following temporarily during compilation
symtab = { '#params' : 0, '#locals' : 0, '#funcs' : 0, '#depth' : 0}
# The scope stack is a stack of such symbol tables. When entering a
# function definition, a semantic action pushes a reference to its
# nestedsymtab onto this stack; when leaving a function definition,
# a semantic action pops an entry from the stack.
# We use a marker nonterminal that expands to epsilon within the
# 'p_funcassign' production below, to push the symbol table for its function
# to this stack, and to add parameter ID bindings.
# See the discussion on p[-1] and "6.11 Embedded Actions" in
# ply-3.0/doc/ply.html to see how to get entries from the paramlist
# in p_funcassign *before* parsing the "stmtrest" that may use those
# parameters. The paramlist holds inherited attributes for the lower-level
# stmtrest, that we can pass using a nestedsymtab on this stack.
scopestack = [symtab]   # The global dictionary never gets popped.

# STUDENT
# RUN-TIME ACTIVATION STACK PROTOCOL FOR ASSIGNMENT 5 USING THE STEP VM
# 1. Caller pushes arguments (actual parameters), one at a time, left-to-right,
# onto the data stack. Code generation must assure correct type promotion
# for an int-to-float for a float parameter, or float-to-int truncation for
# an int parameter.
# 2. Caller pushes the static link for the called function as its final,
# implicit argument (actual parameter), which is a copy of the FRAME
# POINTER 'fp' for the function THAT LEXICALLY ENCLOSES the called function.
# This static link may not be the same as the static link or the 'fp' of
# the calling function. If they are peers in the scope tree (same #depth),
# then they share the same static link; if the called function is one
# scope level deeper than the caller, then the caller's 'fp' is the called
# functions static link; otherwise, the caller must generate a series of
# of stack address calculations to get at an outer scope's FP.
# Any called function is nested, at a minimum, in the outermost scope,
# and so it will have a non-None static link at [-1]. The outermost,
# global-level activation frame does not get one of these when it runs,
# nor does it have any arguments.
# 3. A called function can allocate space on the stack for variables at the
# time they are initialized in the source program. Normally a subroutine's
# preamble would just grow the stack frame upon entry. But, since this source
# language requires initialization of variables that are then immutable,
# it can just allocate their space upon their initialization.
# 4. A function in its postamble must pop all local variables, AND the
# incoming fp & arguments before it returns. It then pushes its return value
# onto the data stack and returns. It uses vmStaticData[0] (see above)
# to house a copy of the RETURN expression while adjusting the data stack,
# then pushes vmStaticData[0] to the data stack before returing.
# See additional comments under production function p_expression_funcall.

# BACKPATCHING: Two forms of backpatching are needed to patch up addresses:
# 1) As functions are being compiled, op codes and in-line operands are
# appended into each function's distinct list reference as field [5] of its
# symtab entry (see Note 2. above).
# Any call to a subroutine (STEP_CALL_SECONDARY) compiles the in-line address
# field as a reference to the ['func' ...] symtab entry for the function
# being compiled. At the end of compilation the __link__
# function (I supply its code) moves these arrays into main program memory
# (the vmCode list) and it replaces their references to the ['func' ...]
# symtab entry with offsets into vmCode.
# 2) All conditional and unconditional GOTO instructions associated
# with flow control, primarily p_expression_conditional for the "?:"
# operator, logical && and ||, must include addresses for the GOTOs.
# The compiler must store them as (offset,) 1-tuples in the GOTO in-line data
# field, where offset is the DISTANCE from the address holding the GOTO address
# of that instruction (not the STEP_GOTO op code, but its in-line data)
# to the destination of the jump in the current function's code memory.
# __link__ replaces these (offset,) 1-tuples with absolute memory addresses
# for the GOTO in-line data destinations.

# PARSON helper functions:

# Set a new variable's type and its offset in it defining stack frame.
def setVARtypeOffset(varname, vartype, varoffset):
    symok = True
    curscope = scopestack[-1]
    if (curscope.has_key(varname)):
        symok = False
        conflict = curscope[varname]
        if conflict[0] == 'var':
            terror(NameError, "ERROR, Variable name "   \
                + varname + " near line " + str(__global_line_number__)
                + " conflicts with variable of same name in current scope.")
        elif conflict[0] == 'func':
            terror(NameError, "ERROR, Variable name "   \
                + varname + " near line " + str(__global_line_number__)
                + " conflicts with function of same name in current scope.")
        elif conflict[0] == 'symref':
            terror(NameError, "ERROR, Variable name "   \
                + varname + " near line " + str(__global_line_number__)
                + " conflicts with outer variable or function of same name"
                + " already used in this scope.")
        else:
            terror(NameError, "ERROR, Variable name "   \
                + varname + " near line " + str(__global_line_number__)
                + " conflicts with symbol of same name in current scope.")
    if (symok):
        symentry = ('var', varname, vartype, varoffset)
        curscope[varname] = symentry

# In assn 5 this function returns an ordered triplet consisting of 1) type
# as in assignment #4; 2) the second field is a stack offset for a variable,
# or a function's location in memory for a function; since the function is
# invoked before its memory address is assigned, its location field
# is a reference to the the Python tuple defining the function in its scope:
#   ['func', ID, type, paramlist, nestedsymtab, codeaddress]
# where codeaddress is a Python list while the function is undergoing
# compilation, and is a static offset into the VM code list after
# __link__ing of the function completes.
# 3) the third returned field is the number of static links crossed in
#    going outwards in scopes.
# A NameError (invalid symname) or TypeError of calling a variable as
# a function, or using a function as a variable, returns (None, None, None).
# A FUNCTION CALL WITH A NUMBER OR TYPE OF ARGUMENTS MISMATCH (TypeError)
# RETURNS A TRIPLET OF (type, None, None), returning the return type to allow
# other error checks to continue; do not generate code in that case.
def getSYMtypeOffset(symname, arglist=None):
    # arglist is not None for a function
    frame = len(scopestack) - 1
    curscope = frame
    symentry = None
    deftable = None
    location = None
    if (arglist == None):
        keyword = 'var'
        message = 'variable'
    else:
        keyword = 'func'
        message = 'function'
    while (frame >= 0):
        if (scopestack[frame].has_key(symname)):
            deftable = scopestack[frame]
            symentry = deftable[symname]
            break
        frame -= 1
    if (not symentry):
        terror(NameError, "ERROR, Undefined " + message + " name "   \
            + symname + " used near line " + str(__global_line_number__))
        return (None, None, None)
    depth = curscope - frame
    if symentry[0] == 'symref':
        depth += symentry[2]
        deftable = symentry[3]  # The original, defining symbol table.
        symentry = deftable[symname]
    if symentry[0] != keyword:
        terror(TypeError, "ERROR, Non-" + message + " name "   \
            + symname + " used as a " + message + " near line "  \
            + str(__global_line_number__))
        return (None, None, None)
    if depth > 0 and not scopestack[-1].has_key(symname):
        scopestack[-1][symname] = ("symref", symname, depth, deftable)
    if arglist != None:
        # Type check arglist against parameter list.
        argerror = False
        paramlist = symentry[3]
        if len(arglist) != len(paramlist):
            terror(TypeError, "ERROR, Function call to " + symname  \
                + " near line " + str(__global_line_number__)   \
                + " has incorrect number of arguments.")
            argerror = True
        argix = 0
        while argix < len(arglist) and argix < len(paramlist):
            if arglist[argix][1] != None and paramlist[argix][1][1] != None \
                    and not tcompat(arglist[argix][1], paramlist[argix][1][1]):
                terror(TypeError, "ERROR, Function call to " + symname \
                    + " near line " + str(__global_line_number__)   \
                    + " has incorrect type for argument for parameter " \
                    + paramlist[argix][0])
                argerror = True
            argix += 1
        if argerror:
            return (symentry[2], None, None) # (type, None, None)
    if (keyword == 'var'):
        location = symentry[3]
    elif (type(symentry[5]) == int):        # actual location in VM memory
        location = symentry[5]
    else:
        location = symentry                 # __link__ it later
    return (symentry[2], location, depth)

# The overall parse tree is an immutable sequence of statements.
def p_goal(p):
    'goal : stmtlist'
    p[0] = p[1]

def p_stmtlist(p):
    '''stmtlist : stmtrest statement'''
    # Grow the sequence without mutation.
    p[0] = p[1] + (p[2],)

def p_stmtrest(p):
    '''stmtrest : stmtrest statement
                | epsilon'''
    if p[1] == None:
        p[0] = ()
    else:
        p[0] = p[1] + (p[2],)

def p_statement_assign(p):
    'statement : assign'
    p[0] = p[1]

def p_statement_expr(p):
    'statement : expression SEP'
    if tIsArray(p[1][1]):
        terror(TypeError, "ERROR, cannot print array near line "   \
            + str(__global_line_number__))
    p[0] = ('printexpression', p[1])    # from p[0] = p[1] January 2012

def p_assign(p):
    '''assign : varassign SEP
                | funcassign'''
    p[0] = p[1]

def p_varassign(p):
    'varassign : typedecl ID ASSIGN_OP expression'
    myscope = scopestack[-1]
    numlocals = myscope['#locals']
    setVARtypeOffset(p[2], p[1][1], numlocals)
    myscope['#locals'] = numlocals + 1
    if p[4][1] != None and not tcompat(p[1][1], p[4][1]):
        terror(TypeError, "ERROR, Type mismatch across '=' "   \
            "near line " + str(__global_line_number__))
    # (varassign, ID, type, expression)
    p[0] = ('varassign', p[2], p[1], p[4])

def p_funcassign(p):
    'funcassign : typedecl ID ASSIGN_OP FUNCTION LPAREN paramlist pushToSymTable RPAREN LBRACE stmtrest RETURN expression SEP RBRACE'
    if p[12][1] != None and not tcompat(p[1][1], p[12][1]):
        terror(TypeError, "ERROR, Type mismatch for return "   \
            + "from function " + p[2]    \
            + " near line " + str(__global_line_number__))
    scopestack.pop()        # Pop rightmost dictionary off the stack.
    outerscope = scopestack[-1]
    numfuncs = outerscope['#funcs']
    outerscope['#funcs'] = numfuncs + 1
    # (funcassign, ID, type, paramlist, stmtrest, (return, expression))
    p[0] = ('funcassign', p[2], p[1], p[6], p[10], ('return', p[12]))

# This is a marker nonterminal that derives epsilon.
# I HAVE WRITTEN THIS FUNCTION. THERE IS NO CODE FOR YOU TO WRITE HERE.
# I added some code at the bottom of this function for assignment 5.
# See "6.11 Embedded Actions" in ply-3.0/doc/ply.html.
# The purpose of pushToSymTable is to add the entry for the function being
# formed in the current scope, and then push a new scope for the symbols
# in this function's scope.
# p[-6] holds the forming function's typedecl
# p[-5] holds its ID. p[-1] holds its paramlist.
# Step 0. Add code to make sure that the p[-5] is not a
# duplicate definition in the current top-of-symtab scope.
# Also make sure that the symbol has not already been used in the current
# scope before this definition, i.e., that it is not ambiguous.
# Both conditions constitute a NameError; use terror to report a NameError.
# 1. If the check in step 0 reported a duplicate or ambiguous ID
# binding in the parent scope, do NOT do this step - don't change the parent
# scope. You will do step 2&3 here so that the compiler can look for more errors
# in the function definition. If the function ID is not a duplicate/ambiguous
# in the parent scope, add a ['func', ID, type, paramlist, nestedsymtab, code]
# entry for this ID in the parent scope, using p[-5], p[-6], p[-1], and a
# freshly constructed nestedsymtab constructed here. The freshly constructed
# nestedsymtab must include initialization of #params, #locals, #funcs,
# and #depth properties per instructions at start of this file.
# 2. Push the latter, freshly constructed nestedsymtab to the scopestack.
# Do this even if the ID is a duplicate or ambiguous, so we can check the
# function definition for more errors. Append to the right side of scopestack.
# 3. Add the members of the paramlist to the freshly pushed nestedsymtab
# detecting any duplicate symbol definitions at this new scope from within
# the paramlist itself, as you would for variables created in this function.
def p_pushToSymTable(p):
    'pushToSymTable : epsilon'
    # print "DEBUG p_pushToSymTable", p[-6], p[-5], p[-1]
    p[0] = None
    # PARSON SOLUTION, Step 0:
    funcname = p[-5]
    functype = p[-6][1]
    paramlist = p[-1]
    outerscope = scopestack[-1]
    outerdepth = outerscope['#depth']
    mycode = []
    innerscope = { '#params' : len(paramlist), '#locals' : 0, '#funcs' : 0,
        '#depth' : (outerdepth + 1)}
    symok = True
    if (outerscope.has_key(funcname)):
        symok = False
        conflict = outerscope[funcname]
        if conflict[0] == 'var':
            terror(NameError, "ERROR, Function name "   \
                + funcname + " near line " + str(__global_line_number__)
                + " conflicts with variable of same name in current scope.")
        elif conflict[0] == 'func':
            terror(NameError, "ERROR, Function name "   \
                + funcname + " near line " + str(__global_line_number__)
                + " conflicts with function of same name in current scope.")
        elif conflict[0] == 'symref':
            terror(NameError, "ERROR, Function name "   \
                + funcname + " near line " + str(__global_line_number__)
                + " conflicts with outer variable or function of same name"
                + " already used in this scope.")
        else:
            terror(NameError, "ERROR, Function name "   \
                + funcname + " near line " + str(__global_line_number__)
                + " conflicts with symbol of same name in current scope.")
    # PARSON SOLUTION, Step 1:
    if (symok):
        symentry = ['func', funcname, functype, paramlist, innerscope, mycode]
        # mycode in the tuple above is where we generate code temporarily.
        outerscope[funcname] = symentry
    # PARSON SOLUTION, Step 2:
    scopestack.append(innerscope)
    # PARSON SOLUTION, Step 3:
    # CODE Added for Assn 5: keep track of negative offset into the stack.
    paramOffset = -(len(paramlist)) - 1  # FP is at [-1]
    for param in paramlist:
        setVARtypeOffset(param[0], param[1][1], paramOffset)
        paramOffset += 1

def p_paramlist(p):
    '''paramlist : typedecl ID paramrest
                | epsilon'''
    # sequence of (ID, type) pairs in parameter list
    if p[1] == None:
        p[0] = ()
    else:
        p[0] = ((p[2], p[1]),) + p[3]

def p_paramrest(p):
    '''paramrest : paramrest COMMA typedecl ID
                | epsilon'''
    # See paramlist.
    if p[1] == None:
        p[0] = ()
    else:
        p[0] = p[1] + ((p[4], p[3]),)

def p_expression_binop(p):
    '''expression : expression ADD_OP expression
                  | expression SUBTRACT_OP expression
                  | expression MULTIPLY_OP expression
                  | expression DIVIDE_OP expression
                  | expression MODULO_OP expression
                  | expression EQ_OP expression
                  | expression NE_OP expression
                  | expression GT_OP expression
                  | expression GE_OP expression
                  | expression LT_OP expression
                  | expression LE_OP expression'''
    compat = None
    if (p[1][1] != None and p[3][1] != None):
        if p[2] == r'+':
            compat = tcompat(p[1][1], p[3][1])
            # This compat allows int[] and float[] to be concatenated
            # (resulting in a float[]), or an any[] to be concatenated
            # with an array of any type, resulting in an array of that type.
        else:
            if tIsArray(p[1][1]) or tIsArray(p[3][1]):
                terror(TypeError, "ERROR, illegal operator for arrays: "    \
                    + p[2] + " near line " + str(__global_line_number__))
            elif p[2] in (r'==', r'!=', r'>', r'>=', r'<', r'<='):
                compat = tcompat(p[1][1], p[3][1])
                if compat != None:
                    # Compatible args, comparisons return an int as a boolean.
                    compat = 'int'
            elif p[2] in (r'-', r'*', r'/'):
                compat = tcompat(p[1][1], p[3][1])              \
                        if p[1][1] in ('int', 'float') else None
            elif p[2] == r'%':
                compat = 'int' if p[1][1] == 'int' and p[3][1] == 'int'     \
                    else None
        if not compat:
            terror(TypeError, "ERROR, Type mismatch across operator "   \
                + p[2] + " near line " + str(__global_line_number__))
    # (OP, TYPEORNONE, leftexpression, rightexpression)
    p[0] = (p[2], compat, p[1], p[3])

def p_expression_logand(p):
    'expression : expression LOGAND_OP expression'
    compat = 'int' if p[1][1] == 'int' and p[3][1] == 'int' else None
    if (p[1][1] != None and p[3][1] != None):
        if not compat:
            terror(TypeError, "ERROR, Type mismatch across operator &&"   \
                + " near line " + str(__global_line_number__))
    # (OP, TYPEORNONE, (leftexpression, rightexpression))
    p[0] = ('&&', compat, (p[1], p[3]))

def p_expression_logor(p):
    'expression : expression LOGOR_OP expression'
    compat = 'int' if p[1][1] == 'int' and p[3][1] == 'int' else None
    if (p[1][1] != None and p[3][1] != None):
        if not compat:
            terror(TypeError, "ERROR, Type mismatch across operator ||"   \
                + " near line " + str(__global_line_number__))
    # (OP, TYPEORNONE, (leftexpression, rightexpression))
    p[0] = ('||', compat, (p[1], p[3]))

def p_tilde_op(p):
    'expression : expression TILDE_OP expression'
    # As in C's comma operator, the tilde operator evaluates & discards its
    # left expression.
    compat = p[3][1]
    if tIsArray(p[1][1]):       # The left expression is the one being printed.
        terror(TypeError, "ERROR, cannot ~ print array near line "   \
            + str(__global_line_number__))
        compat = None
    # (tilde, type-of-right-expression, (leftexpression, rightexpression))
    p[0] = ("~", compat, (p[1], p[3]))

def p_expression_uminus(p):
    "expression : SUBTRACT_OP expression %prec UMINUS"
    compat = None
    if p[2][1] != None:
        if p[2][1] == 'string' or tIsArray(p[2][1]):
            terror(TypeError,                                       \
                "ERROR, Non-numeric type at unary '-' near line "   \
                    + str(__global_line_number__))
        else:
            compat = p[2][1]
    # (uminus, TYPEORNONE, rightexpression)
    p[0] = ('uminus', compat, p[2])

def p_expression_unot(p):
    "expression : LOGNOT_OP expression"
    compat = None
    if p[2][1] != None:
        if p[2][1] != 'int':
            terror(TypeError, "ERROR, Non-int type at unary '!' near line " \
                + str(__global_line_number__))
        else:
            compat = 'int'
    # (unot, TYPEORNONE, rightexpression)
    p[0] = ('unot', compat, p[2])

def p_expression_alen(p):
    "expression : ARRAY_LENGTH LPAREN ID RPAREN"
    compat = None
    arraytype, location, outlinks = getSYMtypeOffset(p[3])
    if not tIsArray(arraytype):
        terror(TypeError, "ERROR, Non-array type at ALEN near line " \
            + str(__global_line_number__))
        arraytype = None
    else:
        compat = 'int'      # ARRAY_LENGTH is an int
    # (arraylen, int_or_none, id, array_type_or_none)
    p[0] = ('arraylen', compat, p[3], arraytype)

def p_expression_typecast(p):
    '''expression : INT LPAREN expression RPAREN
                | FLOAT LPAREN expression RPAREN
                | STRING LPAREN expression RPAREN'''
    if tIsArray(p[3][1]):
        terror(TypeError, "ERROR, Array type at " + p[1] + "() near line " \
            + str(__global_line_number__))
    p[0] = ('typecast', p[1], p[3])

def p_expression_conditional(p):
    "expression : expression QUESTION_OP expression COLON_OP expression"
    compat = None
    if p[1][1] != None and p[3][1] != None and p[5][1] != None:
        if p[1][1] != 'int':
            terror(TypeError, "ERROR, Non-int condition at '?:' near line " \
                + str(__global_line_number__))
        elif p[3][1] != p[5][1]:
            if tIsArray(p[3][1]) and tcompat(p[3][1], p[5][1]):
                # One of them might be an any.
                t1 = tBaseType(p[3][1])
                t2 = tBaseType(p[5][1])
                if t1 == 'any' or t1 == t2:
                    compat = t2 + '[]'
                elif t2 == 'any':
                    compat = t1 + '[]'
                else:
                    terror(TypeError,                               \
                        "ERROR, Result type mismatch at '?:' near line " \
                        + str(__global_line_number__))
            else:
                terror(TypeError,                                   \
                    "ERROR, Result type mismatch at '?:' near line " \
                    + str(__global_line_number__))
        else:
            compat = p[3][1]
    # (?:, TYPEORNONE_FOR_EXPRESSIONS_2_AND_3, expr1, expr2, expr3)
    p[0] = ('?:', compat, p[1], p[3], p[5])

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_scalarvalue(p):
    "expression : scalarvalue"
    # Production 'scalarvalue : ' generates code to put value onto data stack.
    p[0] = p[1]

def p_expression_arrayvalues(p):
    "expression : arrayvalues"
    # Production 'arrayvalues : ' generates code to put value onto data stack.
    p[0] = p[1]

# TODO Added ability to slice an array and get back a subarray.
# We may decide not to do this -- more work, can be done in an app function.
def p_expression_name(p):
    "expression : ID subscript"
    compat, location, outlinks = getSYMtypeOffset(p[1])
    # (id, TYPEORNONE, ID [,subscript])
    subscript = None
    if p[2] != None:                # We have a subscript.
        if not tIsArray(compat):
            terror(TypeError,   \
                "ERROR, Array index for non-array near line " \
                    + str(__global_line_number__) + ", ID: " + p[1])
            compat = None
        else:
            subscript = p[2]
            compat = tBaseType(compat)  # a subscripted element is not an array
    if subscript:
        p[0] = ('id', compat, p[1], p[2])
    else:
        p[0] = ('id', compat, p[1])

def p_subscript(p):
    '''subscript : LBRACK expression RBRACK
                 | epsilon'''
    if p[1] == None:
        p[0] = None
    elif not tcompat(p[2][1], 'int'):
        terror(TypeError,   \
            "ERROR, Non-numeric array index near line " \
                + str(__global_line_number__) + ", type: " \
                + p[2][1])
        p[0] = None
    else:
        p[0] = p[2]

def p_expression_funcall(p):
    "expression : ID LPAREN arglist RPAREN"
    compat, location, outlinks = getSYMtypeOffset(p[1], p[3])
    # (funcall, TYPEORNONE, ID, arglist)
    p[0] = ('funcall', compat, p[1], p[3])

def p_arglist(p):
    '''arglist : expression argrest
                | epsilon'''
    if p[1] == None:
        p[0] = ()
    else:
        p[0] = (p[1],) + p[2]

def p_argrest(p):
    '''argrest : argrest COMMA expression
                | epsilon'''
    if p[1] == None:
        p[0] = ()
    else:
        p[0] = p[1] + (p[3],)

def p_scalarvalue(p):
    """scalarvalue : FLOATNUMBER
                | INTNUMBER
                | STRINGCONSTANT"""
    inlineData = None
    if type(p[1]) == str and len(p[1]) > 1 and p[1][0] == "'"       \
            and p[1][-1] == "'":
        # It is a string constant, discard the outer ''
        lexeme = p[1][1:-1]
        p[0] = ('constant', 'string', lexeme)
    elif '.' in p[1]:
        p[0] = ('constant', 'float', p[1])
    else:
        p[0] = ('constant', 'int', p[1])

def p_arrayvalues(p):
    '''arrayvalues : LBRACK arrayelements RBRACK'''
    basetype, elements = p[2]
    if (basetype == None):
        arraytype = None
    else:
        arraytype = basetype + '[]'
    p[0] = ('arrayvalues', arraytype, elements)

def p_arrayelements(p):
    '''arrayelements : expression moreelements
                     | epsilon'''
    if p[1] == None:
        p[0] = ('any', ())
    else:
        basetype, elements = p[2]
        if (basetype != None and p[1][1] != None):
            commontype = tcompat(basetype, p[1][1])
            if (commontype == None):
                terror(TypeError,   \
                    "ERROR, Array element type mismatch near line " \
                        + str(__global_line_number__) + ", types: " \
                        + basetype + ", " + p[1][1])
            elif (tIsArray(commontype)):
                terror(TypeError,   \
                    "ERROR, Array element type is a nested array near line " \
                        + str(__global_line_number__) + ", types: " \
                        + basetype + ", " + p[1][1])
                commontype = None
        else:
            commontype = None
        p[0] = (commontype, (p[1],) + elements)

def p_moreelements(p):
    '''moreelements : COMMA expression moreelements
                    | epsilon'''
    if p[1] == None:
        p[0] = ('any', ())
    else:
        basetype, elements = p[3]
        if (basetype != None and p[2][1] != None):
            commontype = tcompat(basetype, p[2][1])
            if (commontype == None):
                terror(TypeError,   \
                    "ERROR, Array element type mismatch near line " \
                        + str(__global_line_number__) + ", types: " \
                        + basetype + ", " + p[2][1])
            elif (tIsArray(commontype)):
                terror(TypeError,   \
                    "ERROR, Array element type is a nested array near line " \
                        + str(__global_line_number__) + ", types: " \
                        + basetype + ", " + p[2][1])
                commontype = None
        else:
            commontype = None
        p[0] = (commontype, (p[2],) + elements)

def p_typedecl(p):
    '''typedecl : INT arraydecl
                | FLOAT arraydecl
                | STRING arraydecl'''
    if p[2]:
        p[0] = ('typedecl', p[1] + '[]')
    else:
        p[0] = ('typedecl', p[1])

def p_arraydecl(p):         # Added optional array declaration spring 2012
    '''arraydecl : LBRACK RBRACK
                | epsilon'''
    p[0] = (p[1] != None)

def p_epsilon(p):
    'epsilon :'
    p[0] = None

def p_error(p):
    global __global_error__
    global __global_error_string__
    tmperrstring = None
    if p:
        print "Syntax error at '%s'" % p.value, "near line",    \
            __global_line_number__
        tmperrstring = ("ERROR: Syntax error at '%s'" % p.value)    \
            + " near line " + str( __global_line_number__)
    else:
        print "Syntax error at EOF"
        tmperrstring = "ERROR: Syntax error at EOF"
    if __global_error__ == None:
        __global_error__ = SyntaxError
        __global_error_string__ = tmperrstring

import ply.yacc as yacc
yacc.yacc()


class VMOpList(list):
    def append(self, data):
        if (len(self) and
            not isinstance(data, (list, dict, set)) and
            (not isinstance(data, (str, unicode)) or
             self[-1] == "StepOpCode STEP_CONST")):
            data = self._get_const(data)

        super(VMOpList, self).append(data)

    def _get_const(self, data):
        if isinstance(data, (int, long)):
            return "Long %d" % data
        elif isinstance(data, (float, complex)):
            return "Double %f" % data
        else:
            # Don't mess with it if it's already been made into a number.
            if str(data).startswith(("Double ", "Long ", "String ")):
                return data
            return "String %s" % str(data)


def compile(source, optimizationLevel, debugHandle=None):
    # External hook to the parser.
    global __global_error__
    global __global_error_string__
    global symtab
    global scopestack
    global vmCode
    global vmStaticData
    global DirectThreadedVM
    vmCode = VMOpList()
    vmStaticData = [0]
    symtab = { '#params' : 0, '#locals' : 0, '#funcs' : 0, '#depth' : 0 }
    scopestack = [symtab]   # The global dictionary never gets popped.
    parsetree = yacc.parse(source,debug=logging.DEBUG)
    if __global_error__:
        __printDebugTreeTable__(parsetree, symtab)
        tmperror = __global_error__
        tmpstring = __global_error_string__
        __global_error__ = None             # reset for next time
        __global_error_string__ = None
        raise tmperror, tmpstring
    if optimizationLevel > 0:
        opt = TreeOptimizer(optimizationLevel)
        opttree = opt.optimize(parsetree, symtab)
    else:
        opttree = parsetree
    codegen = CodeGenerator()
    try:
        codegen.generate(opttree, symtab, vmCode, vmStaticData)
    except Exception, msg:
        msg = str(msg)
        sys.stderr.write("INTERNAL ERROR FROM CODE GENERATOR: " + msg + '\n')
        __printDebugTreeTable__(parsetree, symtab, opttree)
        raise
    debugFuncLines = __link__(vmCode, symtab, debugHandle)
    if __global_error__:
        __printDebugTreeTable__(parsetree, symtab, opttree)
        tmperror = __global_error__
        tmpstring = __global_error_string__
        __global_error__ = None             # reset for next time
        __global_error_string__ = None
        raise tmperror, tmpstring
    return ((parsetree, opttree, copy.copy(symtab), copy.copy(vmCode),  \
        copy.copy(vmStaticData)))

def __link__(codearray, symtable, dumpfile):
    # return address-to-funcname map
    #       ID : ['func', ID, type, paramlist, nestedsymtab, codeaddress]
    global __global_error__
    global __global_error_string__
    instrType = type(codearray[0])
    result = { 0 : 'outermost scope' }
    codearray.append("StepOpCode STEP_PAUSE")
    # Stop the VM at end of outer scope.
    def helpLink(scope, table):
        tvals = table.values()
        tvals.sort()    # Try to reduce arbitrary diffs in function order.
        for v in tvals:
            if not (type(v) == list and v[0] == 'func'):
                continue
            if type(v[5] != int):   # Code address is an array not an offset
                offset = len(codearray)
                codearray.extend(v[5])
                v[5] = offset
                result[offset] = scope + "::" + v[1]
            helpLink(scope + "::" + v[1], v[4])
    helpLink('outer scope', symtable)
    if (dumpfile):
        dumpfile.write("PROGRAM MID LINK BEFORE BACKPATCHING:\n")
        dumpMemory(dumpfile, codearray, result)
    # backpatch stage
    for i in xrange(0, len(codearray)):
        t = type(codearray[i])
        if (t == tuple and len(codearray[i]) == 1                   \
                and type(codearray[i][0]) == int) :
            jumploc = i + codearray[i][0] ;
            if (jumploc < 0 or jumploc >= len(codearray)):
                message = "INTERNAL ERROR, invalid jump offset at " \
                    + str(i) + " of " + str(codearray[i])           \
                    + " would goto " + str(jumploc)                 \
                    + " outside memory bound " + str(len(codearray)) + "."
                if (dumpfile):
                    dumpfile.write(message + '\n')
                sys.stdout.write(message + '\n')
                sys.stderr.write(message + '\n')
                __global_error_string__ = message
                __global_error__ = ValueError
            else:
                codearray[i] = jumploc
        elif (t == list and len(codearray[i]) >= 6                  \
                and codearray[i][0] == 'func'                       \
                and type(codearray[i][5]) == int):
            jumploc = codearray[i][5]
            codearray[i] = jumploc
        elif t != int and t != instrType and t != float and t != str:
            message = "INTERNAL ERROR, invalid instruction at " \
                + str(i) + ": " + str(codearray[i]) + "."
            if (dumpfile):
                dumpfile.write(message + '\n')
            sys.stdout.write(message + '\n')
            sys.stderr.write(message + '\n')
            __global_error_string__ = message
            __global_error__ = ValueError
        #elif t != str:
        #    codearray[i] = codearray[i]
    if (dumpfile):
        dumpfile.write("PROGRAM LINK AFTER BACKPATCHING:\n")
        dumpMemory(dumpfile, codearray, result)

__STEP_RE__ = re.compile("STEP_[A-Za-z0-9_]*")
def dumpMemory(dumpfile, dumpcode, dumplabels):
    boundaries = set(dumplabels.keys())
    offset = 0
    for op in dumpcode:
        if offset in boundaries:
            dumpfile.write(str(offset) + "*\tFUNCTION "             \
                + str(dumplabels[offset]) + "\t***************\n")
        op = str(op)
        match = __STEP_RE__.search(op)
        if (match):
            dumpfile.write(str(offset) + ":\t" + match.group() + "\n")
        else:
            dumpfile.write(str(offset) + ":\t" + op + "\n")
        offset += 1

def __printDebugTreeTable__(parsetree, symtab, opttree=None):
    sys.stdout.write('DEBUGGING DUMP OF PARSE TREE:\n')
    printer = PrettyPrinter(indent=4, width=80, stream=sys.stdout)
    printer.pprint(parsetree)
    if opttree and not opttree is parsetree:
        sys.stdout.write('DEBUGGING DUMP OF REWRITTEN PARSE TREE:\n')
        printer.pprint(opttree)
    sys.stdout.write('DEBUGGING DUMP OF SYMBOL TABLE:\n')
    printSymtab(symtab)

if __name__=='__main__':
    while 1:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s: continue
        yacc.parse(s)   # yacc.parse(s, debug=logging.DEBUG)
