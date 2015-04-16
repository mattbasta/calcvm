#       makefile for newvm3 project
#       Programming Assignment 3, CSC526, Spring 2012, Dr. Dale Parson.

all:		build

TARGET = newvm3
DEBUG = 1

include ./makelib

build:

clean:		subclean
		/bin/rm -f *.out *.dif *.pyc junk parsetab.py *.vmlf
		# cd ./stepvm && $(MAKE) clean

test:		clean testparson testbugfix testvectors testbenchmarks testo1 testo2 teststudent

testvm:
			cd ./stepvm && $(MAKE) test

testparson:
		python test_parser.py program1.txt program1.vmlf program1.debug.out > program1.out 2>program1.err.out
		diff program1.out program1.ref  > program1.dif
		-diff program1.debug.out program1.debug.ref > program1.debug.dif
		-python test_parser.py program2.txt program2.vmlf > program2.out 2>program2.err.out
		diff program2.out program2.ref  > program2.dif
		python test_parser.py program3.txt program3.vmlf program3.debug.out > program3.out 2>program3.err.out
		diff program3.out program3.ref  > program3.dif
		-diff program3.debug.out program3.debug.ref  > program3.debug.dif
		python test_parser.py program4.txt program4.vmlf program4.debug.out > program4.out 2>program4.err.out
		diff program4.out program4.ref  > program4.dif
		-diff program4.debug.out program4.debug.ref  > program4.debug.dif
		python test_parser.py program5.txt program5.vmlf program5.debug.out > program5.out 2>program5.err.out
		diff program5.out program5.ref  > program5.dif
		-diff program5.debug.out program5.debug.ref  > program5.debug.dif
		python test_parser.py program6.txt program6.vmlf program6.debug.out > program6.out 2>program6.err.out
		diff program6.out program6.ref  > program6.dif
		-diff program6.debug.out program6.debug.ref  > program6.debug.dif

teststudent:
		python test_parser.py testprogram1.txt testprogram1.vmlf testprogram1.debug.out > testprogram1.tmp.out 2>testprogram1.err.out
		diff testprogram1.tmp.out testprogram1.ref > testprogram1.dif
		python test_parser.py testprogram1.txt testprogram1.vmlf testprogram1.debug.out > testprogram1.o2.out 2>testprogram1_o2.err.out
		diff testprogram1.o2.out testprogram1.o2.ref > testprogram1.o2.dif

testbugfix:
		python test_parser.py program7.txt program7.vmlf program7.debug.out > program7.out 2>program7.err.out
		diff program7.out program7.ref  > program7.dif
		-diff program7.debug.out program7.debug.ref  > program7.debug.dif

testvectors:
		bash ./isPythonNotBill
		python test_parser.py program8.txt program8.vmlf program8.debug.out O0 > program8.out 2>program8.err.out
		diff program8.out program8.ref  > program8.dif
		-diff program8.debug.out program8.debug.ref  > program8.debug.dif
		python test_parser.py program9.txt program9.vmlf program9.debug.out O0 > program9.out 2>program9.err.out
		diff program9.out program9.ref  > program9.dif
		-diff program9.debug.out program9.debug.ref  > program9.debug.dif

testbenchmarks:
		bash ./isPythonNotBill
		time sh -c "python test_parser.py program10.txt program10.vmlf program10.debug.out O0 > program10.out 2>program10.err.out"
		diff program10.out program10.ref  > program10.dif
		-diff program10.debug.out program10.debug.ref  > program10.debug.dif
		time sh -c "python test_parser.py program10.txt program10_O1.vmlf program10_O1.debug.out O1 > program10.out 2>program10.err.out"
		diff program10.out program10_O1.ref  > program10.dif
		-diff program10_O1.debug.out program10_O1.debug.ref  > program10.debug.dif
		time sh -c "python test_parser.py program10.txt program10_O2.vmlf program10_O2.debug.out O2 > program10.tmp.out 2>program10.err.out"
		sed -e "s/<Recursion.*>/CYCLIC SYMTAB PTR/g" -e "s/[0-9][0-9]*]/NNN]/g" program10.tmp.out > program10.out
		diff program10.out program10_O2.ref  > program10.dif
		-diff program10_O2.debug.out program10_O2.debug.ref  > program10.debug.dif

testo1:
		bash ./isPythonNotBill
		time sh -c "python test_parser.py program4.txt program4_O1.vmlf program4_O1.debug.out O1 > program4.out 2>program4.err.out"
		diff program4.out program4_O1.ref  > program4.dif
		-diff program4_O1.debug.out program4_O1.debug.ref  > program4.debug.dif
		python test_parser.py program8.txt program8_O1.vmlf program8_O1.debug.out O1 > program8.out 2>program8.err.out
		diff program8.out program8_O1.ref  > program8.dif
		-diff program8_O1.debug.out program8_O1.debug.ref  > program8.debug.dif
		time sh -c "python test_parser.py program6.txt program6_O1.vmlf program6_O1.debug.out O1 > program6.out 2>program6.err.out"
		diff program6.out program6_O1.ref  > program6.dif
		-diff program6_O1.debug.out program6_O1.debug.ref  > program6.debug.dif

testo2:
		bash ./isPythonNotBill
		python test_parser.py program8.txt program8_O2.vmlf program8_O2.debug.out O2 > program8.tmp.out 2>program8.err.out
		sed -e "s/<Recursion.*>/CYCLIC SYMTAB PTR/g" -e "s/[0-9][0-9]*]/NNN]/g" program8.tmp.out > program8.out
		diff program8.out program8_O2.ref  > program8.dif
		-diff program8_O2.debug.out program8_O2.debug.ref  > program8.debug.dif
		time sh -c "python test_parser.py program6.txt program6_O2.vmlf program6_O2.debug.out O2 > program6.tmp.out 2>program6.err.out"
		sed -e "s/<Recursion.*>/CYCLIC SYMTAB PTR/g" -e "s/[0-9][0-9]*]/NNN]/g" program6.tmp.out > program6.out
		diff program6.out program6_O2.ref  > program6.dif
		-diff program6_O2.debug.out program6_O2.debug.ref  > program6.debug.dif
