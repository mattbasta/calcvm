# TypeChecks.py, initial code by D. Parson, January 2012,
# for use in CSC 526, Compiler II, Spring 2012.
# Utility functions for type checking and symbol table printing.
# This file basically holds utility functions that other modules in
# this package must import. Module dependencies must be acyclic.

def tIsArray(t):
    '''
    Return True if parameter t is a string containing ']' -- array
    types are represented as 'int[]' 'float[]' or 'string[]' --
    otherwise return False.
    '''
    return type(t) == str and ']' in t

def tBaseType(t):
    '''
    Return the base type of parameter t if t is a string containing ']'
    -- array types are represented as 'int[]' 'float[]' or 'string[]' --
    otherwise return t. The base type is 'int' 'float' 'string' or 'any'
    (for type 'any[]' of a zero-length array constant).
    '''
    return t if (not tIsArray(t)) else t[0:-2]  # strips off the '[]' part.

def tcompat(a, b):  # Return the compatible type or None if there is none.
    if (a == b):
        return a
    if (a == None or b == None):
        return None
    numtypes = ('int', 'float')
    if ((a in numtypes) and (b in numtypes)):
        return 'float'
    
    # any[] added for empty arrays when the base type is not known
    # for an array of 0 elements. Spring 2012. If they are both any[]
    # then they are both empty.
    if (a == 'any[]' or b == 'any[]') and tIsArray(a) and tIsArray(b):
        return (b if a == 'any[]' else a)
    # scalar any values happen only when comparing array base types
    if (a == 'any' or b == 'any') and not (tIsArray(a) or tIsArray(b)):
        return (b if a == 'any' else a)

    # Also added for arrays -- an array of base type float is compatible
    # with an array of base type int, although the code generator will
    # have some work to do.
    if tIsArray(a) and tIsArray(b):
        basea = tBaseType(a)
        baseb = tBaseType(b)
        if ((basea in numtypes) and (baseb in numtypes)):
            return 'float[]'
    return None

def printSymtab(stab, scope="global"):
    '''
    Print symbol table for symbol table stab, wher scope is a string to
    print showing the outermost scope name of this symbol table, defaulting
    to 'global'. Output goes to stdout.
    '''
    keys = stab.keys()
    keys.sort()
    for k in keys:
        entry = stab[k]
        if type(entry) == int:      # one of the counters
            print "counter", k, ":", entry
        elif k == "#code":
            print "INTERNAL ERROR, #code tag left behind"
            continue
        elif entry[0] == 'var':
            print ("var " + entry[2] + " " + scope + "::" + entry[1]    \
                + ", frame offset: " + str(entry[3]))
        elif entry[0] == 'symref':
            print ("symref " + entry[1] + " from scope " + scope    \
                + ", depth of " + str(entry[2]))
        elif entry[0] == 'func':   # function, a nested scope
            # print "DEBUG PPP", entry
            print ("function " + entry[2] + " " + scope + "::" + entry[1])
            printSymtab(entry[4], scope + "::" + entry[1])
