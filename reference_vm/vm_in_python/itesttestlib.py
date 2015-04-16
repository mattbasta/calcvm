# Package vm_in_python, module itesttestlib, D. Parson, February 14, 2009
# CSC 580, Spring, 2009, initial threaded code VM examples in Python.
# test code for vm.py

import exceptions
from vm import *
import testlib

vm = IndirectThreadedVM()

code, data, procdbg, datdbg, pcdbg = testlib.loadivm(vm)

try:
    vm.run(code, data)
except VMHaltException, haltcode:
    print "VM halted with exit code " + str(haltcode)
except VMPauseException:
    print "VM hit pause instruction"
except VMBptException:
    print "VM hit breakpoint instruction"
except Exception, estr:
    print "Exception from VM, ip = " + str(vm.ip) + ", ds = "   \
        + str(vm.ds)
    raise
