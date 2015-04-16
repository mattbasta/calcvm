# Package vm_in_python, module testvm, D. Parson, February 1, 2009
# CSC 580, Spring, 2009, initial threaded code VM examples in Python.
# test code for vm.py
# Modified January 2012 for Compiler II -- the VM now takes unbound
# method references as op codes, instead of method bound to a specific
# vm object.

import exceptions
from vm import *

vm = DirectThreadedVM()

# Here is what a compiler creates:
data = [ 3 ]    # Values for data dictionary.
code = [        # Values for code dictionary.
    DirectThreadedVM.STEP_PUSH_FP,                    # added 11/2011
    DirectThreadedVM.STEP_PRINT,
    DirectThreadedVM.STEP_CRLF,
    DirectThreadedVM.STEP_CONST,
    5.1,  # Pass a parameter, formerly a local temporary inside the subroutine
    DirectThreadedVM.STEP_CALL_SECONDARY,
    9,  # subroutine address in this dictionary
    DirectThreadedVM.STEP_GOTO,
    24,                             # jump to last instruction (STEP_NOOP)
    DirectThreadedVM.STEP_PUSH_FP,  # added 11/2011 , start of subroutine
    DirectThreadedVM.STEP_PRINT,
    DirectThreadedVM.STEP_CRLF,
    DirectThreadedVM.STEP_PUSH_FP,                    # added 11/2011
    DirectThreadedVM.STEP_CONST,
    -1,
    DirectThreadedVM.STEP_ADD,
    DirectThreadedVM.STEP_FETCH_STACK,     # fetch parameter based on FP
    DirectThreadedVM.STEP_CONST,
    0,  # offset into data dictionary
    DirectThreadedVM.STEP_FETCH,
    DirectThreadedVM.STEP_ADD,
    DirectThreadedVM.STEP_PRINT,
    DirectThreadedVM.STEP_CRLF,
    DirectThreadedVM.STEP_RETURN,
    DirectThreadedVM.STEP_NOOP,            # last instruction at address 24
    DirectThreadedVM.STEP_CONST,
    'This is a test string.',
    DirectThreadedVM.STEP_PRINT,
    DirectThreadedVM.STEP_CRLF,
    DirectThreadedVM.STEP_CONST,
    'This is part ',
    DirectThreadedVM.STEP_CONST,
    'of a concatenated string.',
    DirectThreadedVM.STEP_ADD,
    DirectThreadedVM.STEP_PRINT,
    DirectThreadedVM.STEP_CRLF
]

vm.run(code, data)
