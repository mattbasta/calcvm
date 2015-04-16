#       makefile for newvm3 project, stepvm/ subdirectory
#       Programming Assignment 3, CSC526, Spring 2012, Dr. Dale Parson.

all:		build

TARGET = newvm3stepvm
DEBUG = 1
PACKAGE=newvm3
SUBPACKAGE=stepvm

include ../makelib

build:		$(CLASSFILES) stepvm.jar

clean:		subclean
		/bin/rm -f *.out *.dif *.pyc *.class stepvm.jar

test:		build
			java newvm3.stepvm.StepVM TestLoadFile.txt newvm3.stepvm 1 1024 128 > StepTest1.out
			diff StepTest1.out StepTest1.ref > StepTest1.dif

docs:		$(CLASSFILES)
			javadoc -classpath $$CLASSPATH -package -d $(ACCTWWW)/stepvm -sourcepath ../.. newvm3.stepvm

stepvm.jar:		$(CLASSFILES)
			chmod +x ./makejar
			/bin/rm -f stepvm.jar
			bash -c "cd ../.. && $(PACKAGE)/$(SUBPACKAGE)/makejar"
			cp stepvm.jar ..
