# Module test_parser tests package newvm3 module progcalc.
# CSC 425 assignment 4, Fall 2011, PLY grammar and parse tree of
# Python nested lists and Python symbol tables.
# Extended assignment 5 to test output from a working compiler for a
# DirectThreadedVM virtual machine.

from progcalc import compile
from TypeChecks import printSymtab
from vm_in_python.vm import DirectThreadedVM, VMPauseException
from sys import argv, stdin, stdout, stderr, exit
from pprint import PrettyPrinter
import re
import sys
import os
__commentPattern__ = re.compile("^((\s*)|(\s*#.*))$")
printer = PrettyPrinter(indent=4, width=80, stream=stdout)

if __name__ == '__main__':
    exitstatus = 0
    rfilehandle = None
    # Do this only if this module is executed as the main module.
    rfilehandle = None
    debugfile = None
    optimizationLevel = 0
    if (len(argv) > 2):
        rfilehandle = open(argv[1], "rU") # portable linefeed handling
        objfilehandle = open(argv[2], "w")
        if (len(argv) > 3):
            debugfile = open(argv[3], "w")
            if (len(argv) > 4 and argv[4].startswith('O')):
                optimizationLevel = int(argv[4][1:])
                if (optimizationLevel < 0 or optimizationLevel > 2):
                    sys.stderr.write("Optimimization level "    \
                        + str(optimizationLevel) + " not supported.\n")
                    sys.exit(1)
    else:
        stderr.write(
            "Invalid usage, test driver takes two mandatory file names." \
            + '\n')
        exit(1)
    line = rfilehandle.readline()
    buffer = ''
    while (line):
        if (__commentPattern__.match(line)):
            line = "\n"     # Keep line number intact.
        buffer = buffer + line
        line = rfilehandle.readline()
    rfilehandle.close()
    stacksize = 1000
    if (argv[1].startswith('program')):
        programNumber = int(argv[1].split('.')[0][len('program'):])
        if (programNumber > 7):
            # The recursive vector tests incur some serious space overhead.
            stacksize = 50000
    vm = DirectThreadedVM(dsz=stacksize, tsz=stacksize)
    parsetree, opttree, symtab, codeArray, staticDataArray                   \
        = compile(buffer, optimizationLevel, debugfile)
    objfilehandle.write("PROGRAMMEMORY\n" + str(len(codeArray)) + '\n')
    memix = 0
    for opline in codeArray:
        if type(opline) != str:
            sys.stderr.write("WARNING, vmCode[" + str(memix)        \
                + "] is not a string: " + str(type(opline)) + ": "  \
                + str(opline) + '\n')
        objfilehandle.write(str(opline) + '\n')
        memix += 1
    objfilehandle.write("DATAMEMORY\n" + str(len(staticDataArray)) + '\n')
    memix = 0
    for opline in staticDataArray:
        if not isinstance(opline, (int, str, float, unicode)):
            sys.stderr.write("WARNING, vmData[" + str(memix)        \
                + "] is not a string: " + str(type(opline)) + ": "  \
                + str(opline) + '\n')
        if isinstance(opline, int):
            optype = "Long"
        elif isinstance(opline, (str, unicode)):
            optype = "String"
        elif isinstance(opline, float):
            optype = "Double"
        objfilehandle.write("%s %s\n" % (optype, str(opline)))
        memix += 1
    objfilehandle.close()
    # printer.pprint(parsetree)
    # if not opttree is parsetree:
    #     print "OPTIMIZED", optimizationLevel, "ABSTRACT SYNTAX TREE"
    #     printer.pprint(opttree)
    # printSymtab(symtab)
    # print "PROGRAM EXECUTION:"
    # try:
    #     # vm.run(codeArray, staticDataArray)
    #     cmdstring = "java -jar stepvm.jar %s newvm3.stepvm 1 1024 128" % argv[2]
    #     sys.stderr.write("RUNNING VM: " + cmdstring + '\n')
    #     sys.stderr.flush()
    #     sys.stdout.flush()
    #     jstat = os.system(cmdstring)
    #     if jstat:
    #         sys.stderr.write("VM exited with non-0 status : "   \
    #             + str(jstat) + '.\n')
    #         exitstatus = 1
    #     else:
    #         sys.stderr.write("VM exited normally.\n");
    # except Exception, exstr:
    #     print "ERROR during VM execution", str(exstr)
    #     stdout.flush()
    #     stderr.flush()
    #     raise       # Re-throw exception that got us here, for stack trace.
    # if debugfile:
    #     #vm.__debugHeap__(debugfile)
    #     debugfile.close()
    sys.exit(exitstatus)
