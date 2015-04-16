#       makefile for CSC 580 assignment 2
#       STEP VM, assembler

#       CSC580, Spring, 2009, Dr. Dale Parson.

all:		build

TARGET = selsort.py

include ./makelib

build:		test

clean:		subclean
		/bin/rm -f *.out *.dif *.out
		# /bin/rm -f *.out *.dif selsort.py testlib.py *.out

# ADD SOME TESTS BELOW AS REQUIRED BY THE ASSIGNMENT HANDOUT.
test:		testassem testbasic testselsort testtestlib itestselsort itesttestlib

testassem:
			echo "tclsh testassem.tcl"
			grep -v vm_in_python < selsort.py > selsort.py.out
			diff selsort.py.out selsort.py.ref > selsort.py.dif
			grep -v vm_in_python < testlib.py > testlib.py.out
			diff testlib.py.out testlib.py.ref > testlib.py.dif

testbasic:
			python testvm.py > testvm.out
			diff testvm.out testvm.ref > testvm.dif

testselsort:
			python testselsort.py > testselsort.out
			diff testselsort.out testselsort.ref > testselsort.dif

testtestlib:
			python testtestlib.py > testtestlib.out
			diff testtestlib.out testtestlib.ref > testtestlib.dif

itestselsort:
			echo "Support for the Indirect Threaded VM eliminate 1/2012."
			# python itestselsort.py > itestselsort.out
			# diff itestselsort.out itestselsort.ref > itestselsort.dif

itesttestlib:
			echo "Support for the Indirect Threaded VM eliminate 1/2012."
			# python itesttestlib.py > itesttestlib.out
			# diff itesttestlib.out itesttestlib.ref > itesttestlib.dif
