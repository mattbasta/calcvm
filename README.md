# CalcVM

Not really a VM at all. This is a compiler for the STEP language developed by Dr. Dale Parson as part of the 2012 Compiler II course at Kutztown University. The language was divided into two parts: a Python parser and bytecode generator, and a Java-based virtual machine (not JVM-based, it was an interpreter written in Java). The Python component would output a bytecode file, which the Java interpreter would then execute. The language featured very basic primitives, safe multithreading, and reference counting garbage collection.

This repository contains the source code for a Python-based transpiler. When given a bytecode file, the transpiler will generate an equivalent C++ file which can be compiled with GCC to produce native code. This has substantial benefits over the Java implementation, namely the use of native pthreads, faster startup times, and the ability to optimize away certain types of operations (e.g., eliminating unnecessary calls to the garbage collector).

A copy of the reference VM can be found in the `reference_vm/` directory, along with a pure Python implementation (both bytecode generator as well as interpreter).


## Usage

These instructions are not guaranteed to work:

```bash
./generate.py path/to/bytecode.vmlf
cp raw/* buildbox/
cd buildbox
make build
```

Using the bytecode generator:

```bash
cd reference_vm
python test_parser.py path/to/sourcecode.txt path/to/bytecode.vmlf
```

Using the reference Java VM:

```bash
cd reference_vm
java -jar stepvm.jar path/to/bytecode.vmlf stepvm 1 1024 128
```


## Exceptions

The following is a complete listing of all exceptions which are intentionally
thrown within compiled applications:

- **1000**: Requested Long value from object of incompatible type.
- **1001**: Requested Double value from object of incompatible type.
- **1002**: Requested String value from object of incompatible type.
- **1999**: Attempting to use stack object that has already been used.
- **2000**: Casting to Long from unsupported type.
- **2001**: Casting to Double from unsupported type.
- **2002**: Casting to String from unsupported type.
- **3000**: Referencing offset past end of array.
- **5000**: Referencing heap object that has already been GCed.


## Restrictions

- The compiler assumes that the code generator will not pass unevaluated
  references to values within arrays outside of the local stack context. This
  means that any value created using `PADD` may not be passed or returned to or
  from a function, passed between threads, passed within lexical scope, etc.
- The compiler assumes that the code generator will not re-use pointers to
  offsets within arrays (generated with `STEP_PADD`).
