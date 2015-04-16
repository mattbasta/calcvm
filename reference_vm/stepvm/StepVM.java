/*
    StepVM.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
import java.util.Arrays ;
import java.util.concurrent.atomic.AtomicLong ;
import java.util.concurrent.ConcurrentHashMap ;
import net.jcip.annotations.* ;

/**
 *  StepVM is the STack-based Emulated Processor (STEP) Virtual Machine (VM)
 *  first used in Compiler Design II, Spring 2012, based on prior VM
 *  implementations in C++ and Python, while adding support for
 *  multithreading on multiprocessors. The Javadoc documentation includes
 *  package-level access for most fields, because the op codes reside
 *  in other classes within this package.
 *  @see StepOpCode
 *  @author Dr. Dale Parson
**/
@ThreadSafe
public class StepVM {
    // Most fields are package-accessible for reasons cited above.
    /** contextCount gives the number of emulated hardware threads. **/
    final int contextCount ;    // number of emulated hardware threads
    /**
     *  ip is the instruction pointer into programMemory, with one
     *  ip per hardware thread, i.e., there are ip[contextCount] registers.
     *  @see StepVM#programMemory
    **/
    final int [] ip ;
    /**
     *  ds is the top pointer into a context's dataStack, with one
     *  ds per hardware thread, i.e., there are ds[contextCount] registers.
     *  @see StepVM#dataStack
    **/
    final int [] ds ;
    /**
     *  fp is the activation frame pointer into a context's dataStack, with one
     *  fp per hardware thread, i.e., there are fp[contextCount] registers.
     *  @see StepVM#dataStack
    **/
    final int [] fp ;
    /**
     *  cs is the top pointer into a context's controlStack, with one
     *  cs per hardware thread, i.e., there are cs[contextCount] registers.
     *  Previous STEP VMs used "ts" and "thread_stack" in place of
     *  "cs" and "controlStack" in this VM.
     *  @see StepVM#controlStack
    **/
    final int [] cs ;
    /**
     *  programMemory holds the contents of a VM program, consisting
     *  of the following four types of Objects.
     *  Each entry is one of the following four types:
     *  1. A reference to a StepOpCode gives a VM machine code instruction.
     *  2. A java.lang.Long gives an int in-line operand for an op code.
     *  3. A java.lang.Double gives a float in-line operand for an op code.
     *  4. A java.lang.String gives a String in-line operand for an op code.
     *  @see StepVM#ip
    **/
    final Object [] programMemory ;
    /**
     *  The dataStack holds data and function activation frames for an
     *  emulated hardware context (hardware thread). Each emulated thread
     *  has its own dataStack, which emulates disjoint memory-mapped regions
     *  holding thread stacks in an operating system such as Unix.
     *  dataStack[contextCount][stackLocation] is indexed by the
     *  context (hardware thread) number as its first index, and by the
     *  offset into the stack (such as ds or fp) as its second index.
     *  emulated hardware context (hardware thread). Each emulated thread
     *  has its dataStack, which emulates disjoint memory-mapped regions
     *  holding thread stacks in an operating system such as Unix.
     *  dataStack[contextCount][stackLocation] is indexed by the
     *  context (hardware thread) number as its first index, and by the
     *  offset into the stack (such as ds or fp) as its second index.
     *  A StepOpCode must grow the dataStack and controlStack for its
     *  hardware thread (context) if needed by the instruction.
     *  Each entry is one of the following four types:
     *  1. A java.lang.Long gives an int datum.
     *  2. A java.lang.Double gives a float datum.
     *  3. A java.lang.String gives a String datum.
     *  4. An internal, opaque type (HeapData) for managing memory regions.
     *  allocated on the heap.
     *  @see StepVM#ds
     *  @see StepVM#fp
    **/
    final Object [][] dataStack ;
    /**
     *  dataStack is allocated an grows by a minimum of DATASTACKGROWSIZE
     *  whenever it grows.
     *  @see StepVM#dataStack
    **/
    public final static int DATASTACKGROWSIZE = 8192 ;
    /**
     *  The controlStack holds stacked frame pointers (fp) and return
     *  addresses during function calls, with fp pushed first and popped last.
     *  Each emulated thread has its own controlStack, which emulates disjoint
     *  memory-mapped regions.
     *  controlStack[contextCount][stackLocation] is indexed by the
     *  context (hardware thread) number as its first index, and by the
     *  offset into the stack (such as cs) as its second index.
     *  A StepOpCode must grow the dataStack and controlStack for its
     *  hardware thread (context) if needed by the instruction.
     *  @see StepVM#cs
     *  @see StepVM#ip
     *  @see StepVM#fp
    **/
    final int [][] controlStack ;
    /**
     *  controlStack is allocated an grows by a minimum of CTRLSTACKGROWSIZE
     *  whenever it grows.
     *  @see StepVM#controlStack
    **/
    public final static int CTRLSTACKGROWSIZE = 512 ;
    /**
     *  dataMemory holds the contents of static storage. The current
     *  implementation of the VM lets the JVM manage heap objects.
     *  Static data consists of the following types of Objects.
     *  Each entry is one of the following four types:
     *  1. A java.lang.Long gives an int datum.
     *  2. A java.lang.Double gives a float datum.
     *  3. A java.lang.String gives a String datum.
     *  4. An internal, opaque type (HeapData) for managing memory regions.
     *  The storage allocator may use additional object types, but they
     *  are not exposed as part of the running program's data.
     *  Code that fetches or stores elements in dataMemory must call
     *  helpFetchDataMemory and helpStoreDataMemory to access the field.
     *  It is private in order to synchronize memory allocation.
    **/
    final Object [] dataMemory ;
    // SOME private implementation data.
    /**
     *  HeapData is an opaque class used by op code classes to allocate and
     *  manage and recover data on the heap. Conceptually a HeapData
     *  object is a reference into the heap, of application type :P.
     *  A HeapData object should be accessed by only 1 thread at a time.
     *  @see STEP_PADD
     *  @see STEP_FETCH
     *  @see STEP_STORE
    **/
    @NotThreadSafe
    class HeapData {
        // Having refCount go < 0 is a bug.
        // Only the final thread to dispense with a reference to a heap
        // region should see refCount go to 0, so assuming no compiler bugs,
        // this class is thread safe without locking. Even with a compiler
        // bug, the worst it will do is to throw StepVMMemoryException or
        // a NullPointerException if used after refcount hits 0.
        /**
         *  Heap data allocated by the JVM allocator.
         *  appdata.length gives the number of application elements.
        **/
        volatile Object [] appData ;
        // appData.length gives the allocated length, it never grows or shrinks
        /**
         *  reference count, Long_MAX_VALUE for do-not-collect, null
         *  for an array offset that is not a first-class array in itself.
         *  A null value distinguishes a second-class array offset pointer
         *  from a first-class array reference, which has a non-null
         *  refCount field.
        **/
        volatile AtomicLong refCount ;
        // reference count, when it hits 0, null appData
        // a refcount of Long.MAX_VALUE is never collected.
        /**
         *  offset is 0 for the reference to the entire array, >= 0
         *  for an offset into an array.
        **/
        final int offset ;
        private final StepVM vm ;
        /**
         *  Construct a full, new array, with data and the initial reference
         *  count. The op code calling this constructor must supply the data
         *  array to other HeapData objects.
        **/
        private HeapData(Object [] data, long initialRefCount) {
            appData = data ;
            refCount = new AtomicLong(initialRefCount);
            offset = 0;
            this.vm = null ;
        }
        /**
         *  Construct a full, new array, with data and the initial reference
         *  count. The op code calling this constructor must supply the data
         *  array to other HeapData objects. The vm will be null if the
         *  HeapData object is constructed before the StepVM object is
         *  fully constructed.
        **/
        private HeapData(Object [] data, long initialRefCount, StepVM vm) {
            appData = data ;
            refCount = new AtomicLong(initialRefCount);
            offset = 0 ;
            this.vm = vm ;
        }
        /**
         *  Construct an element's offset in an array from another array
         *  reference object. The new myOffset is added to the region's
         *  offset, which is logically 0 for the original array reference.
        **/
        private HeapData(HeapData region, int myOffset) {
            appData = region.appData ;
            refCount = null ;
            offset = region.offset + myOffset ;
            vm = region.vm ;
        }
        void addToRefCount(long delta) {
            if (refCount != null && refCount.get() != Long.MAX_VALUE) {
                long rcount = refCount.addAndGet(delta);
                if (rcount < 0L) {
                    throw new StepVMMemoryException(
                        "Dynamic memory region of size " + appData.length
                        + " had reference count decremented to " + rcount,vm);
                } else if (rcount == 0L) {
                    appData = null ;
                    refCount = null ;
                    heapSet.remove(this);
                }
            }
        }
        public String toString() {
            String result ;
            if (appData == null) {
                result = "Freed region detected in dump.";
            } else if (refCount == null) {
                result = "Region offset of [" + offset
                    + "] at heap location " + appData ;
            } else {
                StringBuilder tmpresult =
                    new StringBuilder("Region length " + appData.length
                    + ", refcount = " + refCount.get()
                    + " at heap location " + appData + ":\n") ;
                for (int i = 0 ; i < appData.length ; i++) {
                    tmpresult.append("[" + i + "] = "
                    + ((appData[i] == null) ? "null" : appData[i].toString())
                    + "\n");
                }
                result = tmpresult.toString();
            }
            return result ;
        }
    };
    /**
     *  Package helper to allocate and return a new heap opaque pointer
     *  with reference count of 1.
     *  @param size gives number of elements to allocate.
    **/
    HeapData helpAlloc(int size) {
        if (size == 0) {
            return ZeroElementArray ;
        }
        HeapData result = new HeapData(new Object [size], 1L, this);
        heapSet.put(result, result);
        return result ;
    }
    /**
     *  Package helper to allocate and return a new heap opaque pointer
     *  with reference count of 1.
     *  @param initialData is initial data constructed by the op code.
    **/
    HeapData helpAlloc(Object [] initialData) {
        HeapData result = new HeapData(initialData, 1L, this);
        heapSet.put(result, result);
        return result ;
    }
    /**
     *  Package helper to allocate and return an index element offset.
     *  This methods does not allocate a new array on the heap; it creates
     *  an offset into an existing array.
     *  @param arrayOrIndex is a HeapData reference previously returned by
     *  helpAlloc (as a first-class array reference) or helpIndex (as an
     *  index into an existing array.
     *  @param offsetFromArrayOrIndex is the offset to add to the
     *  reference at arrayOrIndex.
    **/
    HeapData helpIndex(HeapData arrayOrIndex, int offsetFromArrayOrIndex) {
        HeapData result = new HeapData(arrayOrIndex, offsetFromArrayOrIndex);
        return result ;
    }
    /** Dump the state of registers to System.err. **/
    public void dumpRegisters() {
        System.err.println("VM REGISTER DUMP:");
        for (int c = 0 ; c < ds.length ; c++) {
            System.err.println("ip[" + c + "] = " + ip[c]);
            System.err.println("ds[" + c + "] = " + ds[c]);
            System.err.println("fp[" + c + "] = " + fp[c]);
            System.err.println("cs[" + c + "] = " + cs[c]);
            System.err.println("data stack depth[" + c + "] = "
                + dataStack[c].length);
            System.err.println("control stack depth[" + c + "] = "
                + controlStack[c].length);
        }
        System.err.println("program memory length = " + programMemory.length);
        System.err.println("data memory length = " + dataMemory.length);
        System.err.flush();
    }
    /** Dump the allocated heap to System.err as a debugging aid. **/
    public void dumpHeap() {
        System.err.println("HEAP DUMP:");
        for (HeapData entry : heapSet.keySet()) {
            System.err.println(entry.toString());
        }
        System.err.flush();
    }
    // ZeroElementArray is the singleton any[] entry.
    private final HeapData ZeroElementArray ;
    // heapSet used to print dump of non-collected heap regions
    private final ConcurrentHashMap<HeapData,HeapData> heapSet
        = new ConcurrentHashMap<HeapData,HeapData>();
    /**
     *  Construct a StepVM but do not start running it yet.
     *  @param contextCount is the number of emulated contexts (hardware
     *  threads), must be > 0.
     *  @param dataStackSize is the *initial* size of the size of the data
     *  stack allocated for each context. It may grow as needed.
     *  @param controlStackSize is the *initial* size of the size of the
     *  control stack allocated for each context. It may grow as needed.
     *  @param programMemory is the statically allocated program memory.
     *  @param dataMemory is the statically allocated data memory.
     *  @see StepVM#contextCount
     *  @see StepVM#dataStack
     *  @see StepVM#controlStack
     *  @see StepVM#programMemory
     *  @see StepVM#dataMemory
    **/
    public StepVM(int contextCount, int dataStackSize, int controlStackSize,
        Object [] programMemory, Object [] dataMemory) {
        this.contextCount = contextCount ;
        this.dataStack = new Object[contextCount]
            [(dataStackSize >= DATASTACKGROWSIZE)
                ? dataStackSize : DATASTACKGROWSIZE];
        this.controlStack = new int[contextCount]
            [(controlStackSize >= CTRLSTACKGROWSIZE)
                ? controlStackSize : CTRLSTACKGROWSIZE];
        this.programMemory = Arrays.copyOf(programMemory,programMemory.length);
        this.dataMemory = Arrays.copyOf(dataMemory, dataMemory.length);
        ip = new int [ contextCount ] ;     // initialized to zeroes
        ds = new int [ contextCount ] ;     // initialized to zeroes
        fp = new int [ contextCount ] ;     // initialized to zeroes
        cs = new int [ contextCount ] ;     // initialized to zeroes
        ZeroElementArray = new HeapData(new Object [0], Long.MAX_VALUE);
        heapSet.put(ZeroElementArray, ZeroElementArray);
    }
    /**
     *  Run the instructions in program memory until either a STEP_PAUSE
     *  instruction is encountered, throwing StepVMPauseException, or until
     *  some error in compiler-generetd code causes some StepRuntimeException
     *  or other java.lang.RuntimeException to occur. This initial
     *  runs only the main emulated context, thread 0. The op codes for
     *  running worker threads, and infrastructure to support them, will
     *  be added later.
    **/
    public void run() throws StepVMPauseException {
        try {
            while (true) {
                /*
                System.err.println("\nDEBUG ip at " + ip[0]
                    + ", op code " + programMemory[ip[0]]
                    + "\n");
                */
                ((StepOpCode)(programMemory[ip[0]])).eval(this, 0);
            }
        } catch (StepRuntimeException srx) {
            srx.setVM(this);
            throw srx ;
        } catch (RuntimeException rtx) {
            throw new StepRuntimeException("VM chained exception",
                rtx, this);
        }
    }
    /**
     *
     *  Load the load file and construct a VM but do not run the VM.
     *
     *  @param filename is the name of the file to load, with this format:
     *
     *  PROGRAMMEMORY
     *  N (int string giving the length of program memory)
     *  one program memory entry per line
     *  DATAMEMORY
     *  N (int string giving the length of static data memory)
     *  one data memory entry per line
     *
     *  where each entry line has one of the 4 following forms:
     *  Long longValue
     *  Double doubleValue
     *  String doubleValue
     *  StepOpCode opcodeClassname
     *
     *  Example:
     * 
     *  StepOpCode STEP_CONST
     *  Long -2
     *
     *  @param packagePath is the Java package from which to load
     *  StepOpCode class files.
     *  @param contexts is number of contexts (emulated hardware threads)
     *  @param dstacksize is initial size of data stack
     *  @param cstacksize is initial size of control stack
     *  @throws java.io.FileNotFoundException on an invalid file name.
     *  @throws StepRuntimeException for any format problem in the file.
     *
    **/
    public static StepVM load(String filename, String packagePath,
            int contexts, int dstacksize, int cstacksize)
            throws java.io.FileNotFoundException, StepRuntimeException {
        java.util.Scanner scanner = new java.util.Scanner(
            new java.io.File(filename));
        String progmem = scanner.nextLine().trim();
        if (! progmem.equals("PROGRAMMEMORY")) {
            scanner.close();
            throw new StepRuntimeException(
                "PROGRAMMEMORY missing at line 1 of file " + filename + ".",
                    null);
        }
        int psize = (new Integer(scanner.nextLine().trim())).intValue();
        int pcount = 0 ;
        Object [] pmem = new Object[psize] ;
        java.util.HashMap<String, StepOpCode> loaded
            = new java.util.HashMap<String, StepOpCode>();
        for (int i = 0 ; i < psize ; i++) {
            String line = scanner.nextLine();
            String [] lbuf = line.split(" ");
            if (line.startsWith("Long")) {
                pmem[i] = new Long(lbuf[1]);
            } else if (line.startsWith("Double")) {
                pmem[i] = new Double(lbuf[1]);
            } else if (line.startsWith("String")) {
                pmem[i] = line.substring(7);
            } else if (line.startsWith("StepOpCode")) {
                pmem[i] = loaded.get(lbuf[1]);
                if (pmem[i] == null) {
                    try {
                        Class <? extends
                            StepOpCode> opcodeclass
                            = Class.forName(packagePath + "." + lbuf[1]).
                                asSubclass(StepOpCode.class);
                        Class<?> [] consparams = new Class<?> [0];
                        Object [] consargs = new Object [0];
                        java.lang.reflect.Constructor<?
                        		extends StepOpCode> newcons =
                          opcodeclass.getConstructor(consparams);
                        StepOpCode opcodeobj = (StepOpCode)
                            newcons.newInstance(consargs);
                        pmem[i] = opcodeobj ;
                        loaded.put(lbuf[1], opcodeobj);
                    } catch (java.lang.ClassNotFoundException cnx) {
                        System.err.println("Class not found: " + lbuf[1]
                            + ": " + cnx.getMessage());
                        System.exit(3);
                    } catch (java.lang.NoSuchMethodException nnx) {
                        System.err.println("Class constructor not found: "
                            + lbuf[1]
                            + ": " + nnx.getMessage());
                        System.exit(3);
                    } catch (java.lang.InstantiationException inx) {
                        System.err.println("Class constructor error: "
                            + lbuf[1]
                            + ": " + inx.getMessage());
                        System.exit(3);
                    } catch (java.lang.IllegalAccessException anx) {
                        System.err.println("Class constructor access error: "
                            + lbuf[1]
                            + ": " + anx.getMessage());
                        System.exit(3);
                    } catch (java.lang.reflect.InvocationTargetException vnx) {
                        System.err.println("Class constructor call error: "
                            + lbuf[1]
                            + ": " + vnx.getMessage());
                        System.exit(3);
                    } catch (ClassCastException czcx) {
                        System.err.println("Class cast error: "
                            + lbuf[1]
                            + ": " + czcx.getMessage());
                        System.exit(3);
                    } // end try
                }
            } else {
                throw new StepRuntimeException(
                    "Invalid line " + (i+3) + " in file " + filename + ": "
                        + line + ".", null);
            }
        }
        String datamem = scanner.nextLine().trim();
        if (! datamem.equals("DATAMEMORY")) {
            scanner.close();
            throw new StepRuntimeException(
                "DATAMEMORY missing at line "
                + (psize+3) + " of file " + filename + ": " + datamem, null);
        }
        int dsize = (new Integer(scanner.nextLine().trim())).intValue();
        int dcount = 0 ;
        Object [] dmem = new Object[dsize] ;
        for (int i = 0 ; i < dsize ; i++) {
            String line = scanner.nextLine();
            String [] lbuf = line.split(" ");
            if (line.startsWith("Long")) {
                dmem[i] = new Long(lbuf[1]);
            } else if (line.startsWith("Double")) {
                dmem[i] = new Double(lbuf[1]);
            } else if (line.startsWith("String")) {
                dmem[i] = line.substring(7);
            } else {
                throw new StepRuntimeException(
                    "Invalid line " + (psize+i+5) + " in file "
                    + filename + ": " + line + ".", null);
            }
        }
        scanner.close();
        return new StepVM(contexts, dstacksize, cstacksize, pmem, dmem);
    }
    /**
     *  Load the compiled VM program in filename, loading op code classes
     *  from packagePath, and run the VM. See StepVM#load for details on
     *  parameters and load file format.
     *  @return terminated VM for inspection of its state.
     *  @see StepVM#load
    **/
    public static StepVM loadAndRun(String filename, String packagePath,
            int contexts, int dstacksize, int cstacksize)
            throws java.io.FileNotFoundException, StepRuntimeException {
        StepVM vm = load(filename, packagePath, contexts, dstacksize,
            cstacksize);
        vm.run();
        return vm ;
    }
    private static final String usage =
        "StepVM PROGRAMFILE PACKAGEPATH CONTEXTS DSTACKSIZE CSTACKSIZE";
    /**
     *  Load the compiled VM program in args[0], loading op code classes
     *  from package path args[1], numbers of contexts from args[2],
     *  initial data stack size from args[3], initial control stack size from
     *  args[4], and run the VM. See StepVM#load for details on
     *  parameters and load file format.
     *  @see StepVM#load
    **/
    public static void main(String [] args) {
        int exitstatus = 0 ;
        StepVM vm = null ;
        if (args.length != 5) {
            System.err.println(usage);
            System.exit(1);
        }
        try {
            int contexts = Integer.parseInt(args[2]);
            int dstacksize = Integer.parseInt(args[3]);
            int cstacksize = Integer.parseInt(args[4]);
            vm = loadAndRun(args[0], args[1], contexts, dstacksize, cstacksize);
        } catch (java.io.FileNotFoundException fx) {
            System.err.println("File not found: " + args[0]
                + ": " + fx.getMessage());
            System.exit(1);
        } catch (StepVMPauseException px) {
            /*
            System.out.println(
                "Program terminated normally with a PAUSE instruction.");
            */
            System.err.println(
                "Program terminated normally with a PAUSE instruction.");
            vm = px.getVM();
        } catch (StepRuntimeException srx) {
            Throwable cause = srx.getCause();
            if (cause != null) {
                cause.printStackTrace();
                System.err.println(
                    "Target program chained exception: " + cause.getMessage());
                System.err.println("Exception type: "
                    + cause.getClass().toString());
            }
            srx.printStackTrace();
            System.err.println(
                "Target program terminated abnormally: " + srx.getMessage());
            System.err.println("Exception type: " + srx.getClass().toString());
            exitstatus = 1 ;
            vm = srx.getVM();
        } catch (Exception eex) {
            eex.printStackTrace();
            System.err.println(
                "Target program terminated abnormally: " + eex.getMessage());
            System.err.println("Exception type: " + eex.getClass().toString());
            exitstatus = 1 ;
        }
        if (vm != null) {
            vm.dumpRegisters();
            vm.dumpHeap();
        }
        System.exit(exitstatus);
    }
}
