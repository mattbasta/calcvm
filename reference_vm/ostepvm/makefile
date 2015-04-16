#       makefile for newvm3 project, stepvm/ subdirectory
#       Programming Assignment 3, CSC526, Spring 2012, Dr. Dale Parson.

all:		build

TARGET = newvm3stepvm
DEBUG = 1

include ../makelib

build:		$(CLASSFILES)

clean:		subclean
		/bin/rm -f *.out *.dif *.pyc *.class

test:		build

docs:
			javadoc -classpath $$CLASSPATH -package -d $(ACCTWWW) -sourcepath ../.. newvm3.stepvm
