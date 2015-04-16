# testassem.tcl -- assembler test for STEP assembler in Tcl, CSC 552,
# Spring, 2009, D. Parson. Run this in the vm_in_python directory.

source stepsgs.tcl

set fhandle [open selsort.stp r]

set sourcecode [read $fhandle]

close $fhandle

stepCompile $sourcecode "selsort.stp" 1 "selsort.py" w 1

set fhandle [open testlib.stp r]

set sourcecode [read $fhandle]

close $fhandle

stepCompile $sourcecode "testlib.stp" 1 "testlib.py" w 1
