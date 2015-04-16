
build: clean main.out
	chmod +x main.out

debug:
	g++ -g main.cpp -o main.out -lpthread
	gdb main.out

profile:
	g++ -pg main.cpp -o main.prof.out -lpthread
	./main.prof.out
	gprof main.prof.out > report.txt

test: build
	time ./main.out

main.out:
	g++ main.cpp -O2 -o main.out -lpthread

clean:
	rm -rf *.gch
	rm -rf *.o
	rm -rf *.out
	rm -rf core
	rm -rf report.txt
