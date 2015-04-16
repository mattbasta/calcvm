clean:
	rm -rf buildbox/*.cpp buildbox/*.out buildbox/*.out.stackdump buildbox/*.cpp buildbox/*.h buildbox/Makefile buildbox/*.vmlf

test: clean
	python reference_vm/test_parser.py reference_vm/program6.txt buildbox/bytecode.vmlf
	./generate.py buildbox/bytecode.vmlf
	cp raw/* buildbox/
	cd buildbox && chmod 777&& make build && ./main.out
