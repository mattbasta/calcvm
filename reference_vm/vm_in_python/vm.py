# Package vm_in_python, module vm, D. Parson, February 1, 2009
# CSC 580, Spring, 2009, initial threaded code VM examples in Python.
# See documentation for STEP VM and CSC580 assignment 1.
# STUDENTS must implement STEP_ALLOC and STEP_REFCNT using either first-fit
# or best-fit, and coalesce freed regions.

# CSC 526 Compiler II Spring 2012 Enhancements (STUDENT reading):
# 1. Op codes for the DirectThreadedVM are now unbound method references
#    instead of bound method references to a DirectThreadedVM object,
#    so that compilation does not need to bind its output to a specific VM
#    instance. Method resume() (below) now supplies self as an argument to
#    the DirectThreadedVM object. Assembler stepsgs.tcl modified accordingly.
# 2. Support for IndirectThreadedVM removed, and support for it in stepsgs.tcl
#    basically ignored. All IndirectThreadedVM tests are removed.
# 3. Added new op code STEP_DROPN to pop value N off of the data stack and then
#    drop N additional entries off of the data stack. This will speed up
#    postamble processing EXCEPT when there are array local variables or
#    array parameters that need reference count decrements. Note that
#    if N is a negative value, STEP_DROPN actually grows the data stack
#    by abs(N), without initializing values. An N of -1, for example, leaves
#    the slot formerly occupied by N allocated on the data stack. That could be
#    useful in languages that allow local variables to be initialized some
#    time after they are allocated; a preamble would allocate their space using
#    STEP_DROPN with a negative N. See also STEP_DROPFRAME below.
# 4. Added five op codes for allocating and freeing reference-counted arrays
#    into the VM itself. Normally this code would go into a compiled library
#    running on the VM, but for spring 2012 CSC 526 we are building this into
#    the VM in Python. Initially these op codes raise NotImplementedError.
#    The op codes are:
# 4a.STEP_ALLOC pops value N off of the data stack, allocates a region
#    of at least N application locations in the data_dictionary (growing the
#    data_dictionary if necessary while preserving its contents), sets a
#    reference count for that region to 1, and returns the offset of that
#    region in the data_dictionary on the data_stack, replacing value N.
#    The first time STEP_ALLOC is called, it is guaranteed to grow the
#    data_dictionary, because there is no free list of recycled regions.
#    Requesting N < 0 is an error. Requesting N == 0 returns
#    an offset to a fixed, intern'd region containing 0 elements that is
#    never garbaged collected. All 0-element arrays get this same storage
#    location. It contains no space for application data elements.
#    Added a new register "start_of_heap" to the VM that is initialized with
#    the length of the initial data_dictionary. The heap grows starting at
#    that point. See call to __helpInitHeap__ below.
# 4b.STEP_REFCNT pops two values off of the data_stack: a REFCNT_DELTA
#    (on top of the stack) that is a value to add to the reference count, and
#    an OFFSET into the data_dictionary previously returned by STEP_ALLOC but
#    not yet freed, to which the REFCNT_DELTA is added. A positive
#    REFCNT_DELTA increases the reference
#    count. A negative REFCNT_DELTA decreases it, and if it falls to 0
#    (falling < 0 is an error), then the memory manager built into
#    STEP_ALLOC / STEP_REFCNT must free the region and return it to the heap,
#    so it can be reused by a subsequent STEP_ALLOC call. STEP_REFCNT pushes
#    the new reference count onto the data stack, which should be >= 0.
#    If it is 0, then the call to STEP_REFCNT has freed the region.
#    The caller should STEP_DROP this return value if it is not useful.
#    Normally, the REFCNT_DELTA is 1 to add a reference, -1 to remove one,
#    and 0 to query the reference count. If multiple references to a region
#    are being added or deleted at a time, then other REFCNT_DELTA values
#    could be useful. Please note that STEP_ALLOC initializes its region's
#    reference count to 1. It is invalid to invoke STEP_REFCNT on an
#    OFFSET that has never been allocated by STEP_ALLOC, or has subsequently
#    been freed by STEP_REFCNT, or to pass a REFCNT_DELTA that sets the
#    reference count < 0. Those are run-time code errors.
# 4c.STEP_ARRAYCPY pops two values off of the data_stack:
#    a TYPEFLAG (passed on top of the data_stack) that is > 0 for convert
#    cast to float, < 0 for cast to int, and 0 for do not cast.
#    an OFFSET into the data_dictionary previously returned by STEP_ALLOC
#    but not yet freed,
#    It allocates a second array of the same size as
#    the one passed as OFFSET, with a reference count of 1 for the newly
#    created array. It copies all elements from the original array to the
#    copy, optionally applying a Python typecast if TYPEFLAG != 0.
#    It does not modify the reference count of the original array.
#    The return stack carries the OFFSET of the newly allocated array,
#    which can later have its reference count adjusted via STEP_REFCNT.
# 4d.STEP_ARRAYCAT pops three values off of the data_stack:
#    TYPEFLAG (passed on top of the data_stack) that is > 0 for convert
#    cast to float, < 0 for cast to int, and 0 for do not cast.
#    ROFFSET into the data_dictionary previously returned by STEP_ALLOC
#    but not yet freed 
#    LOFFSET into the data_dictionary previously returned by STEP_ALLOC
#    but not yet freed 
#    It allocates a third array that is the concatenation LOFFSET + ROFFSET
#    sizes of the input arrays, with a reference count of 1 for the newly
#    created array. It copies all elements from the LOFFSET array to the
#    copy, then concatenates the ROFFSET elements into the new array,
#    optionally applying a Python typecast if TYPEFLAG != 0.
#    It does not modify the reference count of the original arrays.
#    The return stack carries the OFFSET of the newly allocated array,
#    which can later have its reference count adjusted via STEP_REFCNT.
# 4e.STEP_HEAP pushes the offset of the start of the heap onto the data
#    stack. This is always the length of the initial data_dictionary before
#    the first invocation of STEP_ALLOC. It contains the pointer to the first
#    region in the free list, or None if the free list is empty.
# 5. STEP_DROPFRAME, added for Spring 2012 assignment 2, takes two arguments
#    on the data stack: A BOTTOM_OFFSET and a TOP_OFFSET, with the latter
#    on top of the data stack. After popping these two arguments, it
#    removes all stack elements at [fp+BOTTOM_OFFSET] through [fp+TOP_OFFSET].
#    BOTTOM_OFFSET should normally be < 0 for incoming arguments and the
#    incoming static link. TOP_OFFSET is >= 0 i.f.f. there are local
#    variables. Note that the range is through TOP_OFFSET inclusive.
#    This op code should make optimizing tail calls more effective.

# CSC 425 Compiler I Fall 2011 Parson Enhancements:
# 1. Add the frame pointer 'fp' that points into the base address
#    of the current frame within the data_stack, reset to 0.
#    The usage is for high level languages that want to main an
#    activation frame. A calling subroutine will push its arguments
#    onto the data stack, and then invoke STEP_CALL_SECONDARY as before.
# 2. STEP_CALL_SECONDARY now pushes first the current 'fp' onto the
#    the thread_stack, followed by the 'ip'; previously STEP_CALL_SECONDARY
#    pushed only the 'ip'. STEP_CALL_SECONDARY then loads 'fp' with the
#    current 'ds' (one above top of data stack) and the 'ip' with the
#    subroutine address (as before). STEP_RETURN pops 'ip' and 'fp' now;
#    previously it popped only 'ip' from the thread stack.
# 3. Added instruction STEP_PUSH_FP to push the current 'fp' value
#    onto the data stack.
# 4. Added instruction STEP_FETCH_STACK, similar to the existing STEP_DUP_I
#    instruction. Where STEP_DUP_I duplicates a value using an index
#    from the top of the data stack and pushes its indexed value onto the
#    data stack, STEP_FETCH_STACK replaces an index from the bottom of the data
#    stack (index 0) with the data stack value at that index. STEP_FETCH_STACK
#    works with STEP_PUSH_FP because 'fp' is an index from the bottom of
#    the data stack, just like 'ds'. A compiler can use STEP_PUSH_FP to push
#    'fp' onto the data stack, then add a negative offset to address an
#    argument to a function, or a non-negative offset to address a local
#    variable. STEP_FETCH_STACK then replaces this fp+offset with the data stack
#    location's contents as addressed by that fp+offset. STEP_PUSH_FP can
#    also be used to push 'fp' as an argument before calling a function,
#    e.g., in order to initialize a static link for nested function access
#    to lexically enclosing activation frames.
# 5. Added STEP_STORE_STACK that takes an index (address) on top of the stack,
#    and a value beneath it, and stores the value at the indexed offset
#    (from 0) on the data stack, popping both arguments. It checks to make
#    sure that the current stack below self.ds (after completing the operation)
#    is big enough to hold the result. If it is off-by-one after popping the
#    two arguments to STEP_STORE_STACK, then it adds 1 to self.ds. Otherwise,
#    it prints a warning.
# 6. Added STEP_STORE_I that is the inverse of STEP_DUP_I. Given a non-negative
#    offset on top of the stack and a value beneath it, STEP_STORE_I removes
#    this offset-value pair from the data stack, and stores the value at
#    offset steps from the top of the data stack, where an offset of 0
#    replaces the current top-of-stack after removing the offset-value pair,
#    an offset of 1 replaces the one below that, etc. STEP_STORE_I indexes
#    from the top of the data stack, while STEP_STORE_STACK indexes from
#    the bottom (from offset 0).
# 7. Added STEP_CAST_INT, STEP_CAST_FLOAT and STEP_CAST_STRING that replace
#    the value on the top of the data stack with an int(), float() or str()
#    conversion respectively of that value.
# 8. Added some very basic tests for the new instructions to tesvm.py.

import exceptions
from sys import stdout, stderr, maxint
from pprint import PrettyPrinter

# DEBUGF = open('DEBUGVM.txt', 'w')

class VMException(exceptions.Exception):
    """
    VMException is any Exception from a VM that is not an error.
    """
    def __init__(self, args=None):
        self.args = args

class VMError(exceptions.Exception):
    """
    VMError is any Exception from a VM that is an error.
    """
    def __init__(self, args=None):
        self.args = args

class VMPauseException(VMException):
    pass

class VMHaltException(VMException):
    pass

class VMBptException(VMException):
    pass

class DirectThreadedVM(object):
    """ A Direct Threaded VM, modeled after the Forth and STEP VMs. """
    ##############  MACHINE SETUP AND CONTROL ###################
    default_stacksize = 1000 # class static value
    hexformat = "0x%x"
    octalformat = "0%o"
    decimalformat = "%d"
    def __init__(self, dsz=default_stacksize, tsz=default_stacksize,    \
            codedict=[], datadict=[]):
        #self.__helpInitHeap__()
        pass
    def run(self, codedict=None, datadict=None, stepcount=None):
        """ Start the machine from the beginning, with an empty heap. """
        if (codedict):
            self.code_dictionary = codedict
        if (datadict):
            self.data_dictionary = datadict
            self.start_of_heap = len(datadict)
            self.__helpInitHeap__()
        self.reset()
        self.resume(stepcount)
    def reset(self):
        """ Reset IP and DS and FP and TS to 0 -- empty the stacks. """
        self.ip = 0
        self.ds = 0
        self.fp = 0
        self.ts = 0
    def resume(self, stepcount=None):
        """ Resume the machine after a VMPauseException or VMHaltException """
        if (self.ip < 0 or self.ip >= len(self.code_dictionary)):
            raise VMError, "ip " + str(self.ip) + " points beyond code memory"
        while (self.ip >= 0 and self.ip < len(self.code_dictionary) \
                and (stepcount == None or stepcount > 0)):
            apply(self.code_dictionary[self.ip],(self,))
            if (stepcount > 0):
                stepcount -= 1

    def __getattribute__(self, name):
        if name.startswith("STEP_"):
            return "StepOpCode %s" % name
        else:
            return object.__getattribute__(self, name)
    
    __MEMHDR__ = 0      # Total size of the region, user & administrative data
    __MEMRFC__ = 1      # REFERENCECOUNT below
    __MEMLEN__ = 2      # Number of actual user array elements requested.
    __MEMPRV__ = 2      # PREVIOUS in doubly linked free list node
    __MEMNXT__ = 3      # NEXT in doubly linked free list node
    __MEMAPD__ = 3      # APplication Data is at some spot as __MEMNXT__.
    __MEMOVH__ = 4      # OVERHEAD: __MEMHDR__,__MEMRFC__,__MEMLEN__,FOOTER
    __MEMMINREQ__ = 1   # Minimum size of a user request or __MEMNXT__.
    __MEMMINTOT__ = __MEMOVH__ + __MEMMINREQ__


class OldDirectThreadedVM(object):
    # MICROINSTRUCTION BUILDING BLOCKS
    def __bop__(self, opfun):
        # binary operator that replaces "x y" with "x opfun y" on the ds
        self.ip += 1
        self.ds -= 1
        self.data_stack[self.ds-1] = apply(opfun,                  \
            (self.data_stack[self.ds-1],self.data_stack[self.ds]))
        if (self.data_stack[self.ds-1] == True):
            self.data_stack[self.ds-1] = 1
        elif (self.data_stack[self.ds-1] == False   \
                or self.data_stack[self.ds-1] == None):
            self.data_stack[self.ds-1] = 0
    def __uop__(self, opfun):
        # unary operator that replaces "x" with "opfun x" on the ds
        self.ip += 1
        self.data_stack[self.ds-1] = apply(opfun,                  \
            (self.data_stack[self.ds-1],))
        if (self.data_stack[self.ds-1] == True):
            self.data_stack[self.ds-1] = 1
        elif (self.data_stack[self.ds-1] == False   \
                or self.data_stack[self.ds-1] == None):
            self.data_stack[self.ds-1] = 0
    # PRIMITIVES IN THE STEP VM.
    def STEP_PAUSE(self):
        self.ip += 1
        raise VMPauseException, "pause at " + str(self.ip-1)
    def STEP_BPT(self):
        self.ip += 1
        raise VMBptException, "breakpoint at " + str(self.ip-1)
    def STEP_HALT(self):
        self.ds -= 1
        self.ip += 1
        raise VMHaltException, str(self.data_stack[self.ds])

    def STEP_ADD(self): self.__bop__(lambda x, y : x+y)
    def STEP_SUB(self): self.__bop__(lambda x, y : x-y)
    def STEP_MULT(self): self.__bop__(lambda x, y : x*y)
    def STEP_DIV(self): self.__bop__(lambda x, y : x/y)
    def STEP_MOD(self): self.__bop__(lambda x, y : x%y)
    def STEP_BITAND(self): self.__bop__(lambda x, y : x&y)
    def STEP_BITOR(self): self.__bop__(lambda x, y : x|y)
    def STEP_BITXOR(self): self.__bop__(lambda x, y : x^y)
    def STEP_SHL(self): self.__bop__(lambda x, y : x << y)
    def STEP_SHR(self): self.__bop__(lambda x, y : x >> y)
    def STEP_LOGAND(self):
        self.__bop__(lambda x, y : x and y)
        if (self.data_stack[self.ds-1]):
            self.data_stack[self.ds-1] = 1
        else:
            self.data_stack[self.ds-1] = 0
    def STEP_LOGOR(self):
        self.__bop__(lambda x, y : x or y)
        if (self.data_stack[self.ds-1]):
            self.data_stack[self.ds-1] = 1
        else:
            self.data_stack[self.ds-1] = 0
    def STEP_EQ(self): self.__bop__(lambda x, y : x == y)
    def STEP_NEQ(self): self.__bop__(lambda x, y : x != y)
    def STEP_LT(self): self.__bop__(lambda x, y : x < y)
    def STEP_GT(self): self.__bop__(lambda x, y : x > y)
    def STEP_LE(self): self.__bop__(lambda x, y : x <= y)
    def STEP_GE(self): self.__bop__(lambda x, y : x >= y)
    def STEP_RROT(self):
        """ rrot uses bottom 32 bits of its x operand. """
        def rrot(x, bits):
            x32 = int(x) & 0x0ffffffff
            if (bits < 0 or bits > 32):
                raise VMError, "invalid bit count for STEP_RROT: " + str(bits)
            if (bits > 0 and bits < 32):
                return(int(((x32 >> bits)|(x32 << (32-bits)))&0x0ffffffff))
            else:
                return(int(x32))
        self.__bop__(rrot)
    def STEP_LROT(self):
        """ lrot uses bottom 32 bits of its x operand. """
        def lrot(x, bits):
            x32 = int(x) & 0x0ffffffff
            if (bits < 0 or bits > 32):
                raise VMError, "invalid bit count for STEP_LROT: " + str(bits)
            if (bits > 0 and bits < 32):
                return(int(((x32 << bits)|(x32 >> (32-bits)))&0x0ffffffff))
            else:
                return(int(x32))
        self.__bop__(lrot)
    def STEP_RROT16(self):
        """ rrot uses bottom 16 bits of its x operand. """
        def rrot(x, bits):
            x16 = x & 0x0ffff
            if (bits < 0 or bits > 16):
                raise VMError, "invalid bit count for STEP_RROT16: " + str(bits)
            if (bits > 0 and bits < 16):
                return(int(((x16 >> bits)|(x16 << (16-bits))) & 0x0ffff))
            else:
                return(int(x16))
        self.__bop__(rrot)
    def STEP_LROT16(self):
        """ lrot uses bottom 16 bits of its x operand. """
        def lrot(x, bits):
            x16 = x & 0x0ffff
            if (bits < 0 or bits > 16):
                raise VMError, "invalid bit count for STEP_LROT16: " + str(bits)
            if (bits > 0 and bits < 16):
                return(int(((x16 << bits)|(x16 >> (16-bits))) & 0x0ffff))
            else:
                return(int(x16))
        self.__bop__(lrot)
    def STEP_MINUS(self): self.__uop__(lambda x : - x)
    def STEP_COMPLEMENT(self): self.__uop__(lambda x : ~ x)
    def STEP_SIGN(self): self.__uop__(lambda x : x < 0)
    def STEP_ABS(self):
        """ Python 2.5 added conditional exprs; I'm stuck in 2.4 at home. """
        def abs(x):
            if (x < 0):
                return(-x)
            else:
                return(x)
        self.__uop__(abs)
    def STEP_ZEQ(self): self.__uop__(lambda x : x == 0)
    def STEP_ZNEQ(self): self.__uop__(lambda x : x != 0)
    def STEP_ZLT(self): self.__uop__(lambda x : x < 0)
    def STEP_ZGT(self): self.__uop__(lambda x : x > 0)
    def STEP_ZLE(self): self.__uop__(lambda x : x <= 0)
    def STEP_ZGE(self): self.__uop__(lambda x : x >= 0)
    def STEP_ADD1(self): self.__uop__(lambda x : x + 1)
    def STEP_SUB1(self): self.__uop__(lambda x : x - 1)
    def STEP_ADD2(self): self.__uop__(lambda x : x + 2)
    def STEP_SUB2(self): self.__uop__(lambda x : x - 2)
    def STEP_MULT2(self): self.__uop__(lambda x : x * 2)
    def STEP_DIV2(self): self.__uop__(lambda x : x / 2)
    def STEP_SHL1(self): self.__uop__(lambda x : x << 1)
    def STEP_SHR1(self): self.__uop__(lambda x : x >> 1)
    def STEP_DUP(self):
        self.ip += 1
        self.data_stack[self.ds] = self.data_stack[self.ds-1]
        self.ds += 1
    def STEP_DUP2(self):
        self.ip += 1
        self.data_stack[self.ds] = self.data_stack[self.ds-1]
        self.data_stack[self.ds+1] = self.data_stack[self.ds-1]
        self.ds += 2
    def STEP_DUP_I(self):
        self.ip += 1
        offset = self.data_stack[self.ds-1]
        self.data_stack[self.ds-1] = self.data_stack[self.ds-2-offset]
    def STEP_STORE_I(self):
        self.ip += 1
        offset = self.data_stack[self.ds-1]
        value = self.data_stack[self.ds-2]
        self.data_stack[self.ds-offset-3] = value
        self.ds -= 2
    def STEP_FETCH_STACK(self):
        self.ip += 1
        offset = self.data_stack[self.ds-1]
        self.data_stack[self.ds-1] = self.data_stack[offset]
    def STEP_STORE_STACK(self):
        self.ip += 1
        offset = self.data_stack[self.ds-1]
        value = self.data_stack[self.ds-2]
        self.data_stack[offset] = value
        self.ds -= 2
        if (self.ds == offset):
            # In the process of popping the two arguments to STEP_STORE_STACK,
            # the value just stored got lost because its offset is now
            # beyond top-of-stack. We must fix that.
            self.ds += 1
        elif (self.ds < offset):
            stderr.write("WARNING, a STEP_STORE_STACK of " + str(value) \
                + " at stack offset " + str(offset)                     \
                + " is above highest data stack entry at "              \
                + str(self.ds - 1) + ".")
    def STEP_SWAP(self):
        self.ip += 1
        tmp = self.data_stack[self.ds-1]
        self.data_stack[self.ds-1] = self.data_stack[self.ds-2]
        self.data_stack[self.ds-2] = tmp
    def STEP_SWAP2(self):
        self.ip += 1
        tmp = self.data_stack[self.ds-1]
        self.data_stack[self.ds-1] = self.data_stack[self.ds-3]
        self.data_stack[self.ds-3] = tmp
    def STEP_OVER(self):
        self.ip += 1
        self.data_stack[self.ds] = self.data_stack[self.ds-2]
        self.ds += 1
    def STEP_OVER2(self):
        self.ip += 1
        self.data_stack[self.ds] = self.data_stack[self.ds-3]
        self.ds += 1
    def STEP_DROP(self):
        self.ip += 1
        self.ds -= 1
    def STEP_DROP2(self):
        self.ip += 1
        self.ds -= 2
    def STEP_DROPN(self):
        self.ip += 1
        self.ds -= (self.data_stack[self.ds-1] + 1)
    def STEP_DROPFRAME(self):
        self.ip += 1
        top = self.fp + self.data_stack[self.ds-1]
        bottom = self.fp + self.data_stack[self.ds-2]
        self.ds -= 2
        count = top - bottom + 1
        originalCount = count
        # DEBUGF.write("DEBUG BEFORE DROP FRAME " + str(bottom) + ".." + str(top) + "[" + str(self.ds) + "] @" + str(self.ip) + "\n")
        # DEBUGF.flush()
        beyond = top + 1
        while count > 0 and beyond < self.ds:
            self.data_stack[bottom] = self.data_stack[beyond]
            bottom += 1
            beyond += 1
            count -= 1
        self.ds -= originalCount
        # DEBUGF.write("DEBUG AFTER DROP FRAME " + str(bottom) + ".." + str(top) + "[" + str(self.ds) + "] @" + str(self.ip) + "\n")
        # DEBUGF.flush()
    def STEP_CAST_INT(self):
        self.ip += 1
        self.data_stack[self.ds-1] = int(self.data_stack[self.ds-1])
    def STEP_CAST_FLOAT(self):
        self.ip += 1
        self.data_stack[self.ds-1] = float(self.data_stack[self.ds-1])
    def STEP_CAST_STRING(self):
        self.ip += 1
        self.data_stack[self.ds-1] = str(self.data_stack[self.ds-1])
    def STEP_FETCH(self):
        self.ip += 1
        self.data_stack[self.ds-1] =        \
            self.data_dictionary[self.data_stack[self.ds-1]]
    def STEP_STORE(self):
        self.ip += 1
        self.data_dictionary[self.data_stack[self.ds-1]]    \
            = self.data_stack[self.ds-2]
        self.ds -= 2
    def STEP_PRINT(self):
        self.ip += 1
        stdout.write(str(self.data_stack[self.ds-1]))
        self.ds -= 1
    def STEP_PRINTI(self):
        self.ip += 1
        if (type(self.data_stack[self.ds-1]) == int     \
                or (type(self.data_stack[self.ds-1]) == long \
                    and self.printbase != self.decimalformat)):
            if (self.printbase == self.decimalformat):
                stdout.write(self.printbase         \
                    % self.data_stack[self.ds-1])
            else:
                stdout.write(self.printbase         \
                    % (self.data_stack[self.ds-1] & 0xffffffff))
        else:
            stdout.write(str(self.data_stack[self.ds-1]))
        self.ds -= 1
    def STEP_PRINTS(self):
        self.ip += 1
        datum = self.data_dictionary[self.data_stack[self.ds-1]]
        if (type(datum) == int):
            if (self.printbase == self.decimalformat):
                stdout.write(self.printbase % datum)
            else:
                stdout.write(self.printbase % (datum & 0xffffffff))
        else:
            stdout.write(str(datum))
        self.ds -= 1
    def STEP_CRLF(self):
        self.ip += 1
        print ""
    def STEP_DECIMAL(self):
        self.ip += 1
        self.printbase = self.decimalformat
    def STEP_HEX(self):
        self.ip += 1
        self.printbase = self.hexformat
    def STEP_OCTAL(self):
        self.ip += 1
        self.printbase = self.octalformat
    def STEP_SIZEOF(self):
        self.ip += 1
        self.data_stack[self.ds] = 1
        self.ds += 1
    def STEP_DS_DEPTH(self):
        self.ip += 1
        self.ds += 1
        self.data_stack[self.ds-1] = self.ds
    def STEP_TS_DEPTH(self):
        self.ip += 1
        self.data_stack[self.ds] = self.ts
        self.ds += 1
    def STEP_PUSH_FP(self):
        self.ip += 1
        self.data_stack[self.ds] = self.fp
        self.ds += 1
    def STEP_CODE_DICT_LEN(self):
        self.ip += 1
        self.data_stack[self.ds] = len(self.code_dictionary)
        self.ds += 1
    def STEP_DATA_DICT_LEN(self):
        self.ip += 1
        self.data_stack[self.ds] = len(self.data_dictionary)
        self.ds += 1
    def STEP_NOOP(self):
        self.ip += 1
    def STEP_RETURN(self):
        self.ts -= 2
        self.ip = self.thread_stack[self.ts+1]
        self.fp = self.thread_stack[self.ts]

    # OPERATIONS WITH IP-IN-LINE PARAMETERS THAT CAN BE CURRIED.
    def STEP_CONST(self):
        self.__HELP_STEP_CONST__(self.code_dictionary[self.ip+1],2)
    def __HELP_STEP_CONST__(self, constdata, ipdelta):
        """
        Protected helper for STEP_CONST that takes the constdata value
        and the post-op ipdelta as parameters.
        """
        self.data_stack[self.ds] = constdata
        self.ds = self.ds + 1
        self.ip += ipdelta # get an instruction beyond
    def STEP_VAR(self):
        self.STEP_CONST()
    def STEP_ARRAY(self):
        self.STEP_CONST()
    def STEP_GOTO(self):
        self.ip = self.code_dictionary[self.ip+1]
    def STEP_GOTO0(self):
        self.__HELP_STEP_GOTO0__(self.code_dictionary[self.ip+1],2)
    def __HELP_STEP_GOTO0__(self,jumpaddr,ipdelta):
        """
        If self.data_stack[self.ds-1] == 0 then jump ip to jumpaddr
        Else add ipdelta to ip.
        """
        if (self.data_stack[self.ds-1] == 0):
            self.ip = jumpaddr
        else:
            self.ip += ipdelta
        self.ds -= 1
    def STEP_GOTOX(self):
        self.ds -= 1
        offset = self.data_stack[self.ds] # Get offset into switch table.
        numcases = self.code_dictionary[self.ip+1] # Length of switch table.
        if (offset < 0 or offset >= numcases):
            # Switch is outside the table, use the final default case.
            offset = numcases - 1
        self.ip += 2     # Point to array of case secondary addresses.
        opcode = self.code_dictionary[self.ip+offset] # secondary's opcode
        self.ip += numcases  # Point past the list of secondaries.
        self.code_dictionary[self.ip+1] = opcode
        # Above line jams opcode of selected secondary after a call op.
    def STEP_CALL_SECONDARY(self):
        """ The secondary address follows the instruction in-line. """
        self.thread_stack[self.ts] = self.fp     # save frame pointer
        self.thread_stack[self.ts+1] = self.ip + 2 # save return address
        self.ts += 2
        self.fp = self.ds
        self.ip = self.code_dictionary[self.ip+1] # make the call
    def STEP_HEAP(self):
        self.ip += 1
        self.ds += 1
        self.data_stack[self.ds-1] = self.start_of_heap
    def STEP_ALLOC(self):
        '''
        Allocate a region of size N (passed on the data stack) in the
        data_dictionary's heap, returning the offset (passed on the data
        stack) of where the region resides in the data_dictionary.
        STEP_ALLOC sets the region's reference count to 1 -- see
        reference count comments for STEP_REFCNT. Requesting N < 0
        is an error. Returns reference-counted OFFSET into data_dictionary
        for the array.
        '''
        self.ip += 1
        if (self.data_stack[self.ds-1] < 0):
            raise ValueError, "Request to STEP_ALLOC a negative amount: " \
                + str(self.data_stack[self.ds-1])
        self.data_stack[self.ds-1] = self.__helpAlloc__(
            self.data_stack[self.ds-1])
    def STEP_REFCNT(self):
        '''
        Pops REFCNT_DELTA and then OFFSET from the data_stack, then
        adds REFCNT_DELTA (it may be negative) to the reference count
        at region OFFSET in the data_dictionary previously returned by
        STEP_ALLOC. STEP_REFCNT returns the new reference count on the
        data_stack, and if it drops to 0, STEP_REFCNT deallocates that
        region and returns it to the heap for later possible allocation
        via STEP_ALLOC.
        '''
        self.ip += 1
        self.data_stack[self.ds-2] = self.__helpRefcount__(
            self.data_stack[self.ds-2], self.data_stack[self.ds-1]);
        self.ds -= 1
        if (self.data_stack[self.ds-1] < 0):
            raise ValueError, "STEP_REFCNT drops below 0 for region "   \
                + str(self.data_stack[self.ds])
    def STEP_ARRAYCPY(self):
        '''
        ARRAYOFFSET TYPEFLAG (top)
        ->
        NEWARRAYOFFSET
        '''
        self.ip += 1
        oldarray = self.data_stack[self.ds-2]
        castflag = self.data_stack[self.ds-1]
        count = self.data_dictionary[oldarray-1]
        newarray = self.__helpAlloc__(count)
        for i in range(0, count):
            value = self.data_dictionary[oldarray+i]
            if (castflag > 0):
                value = float(value)
            elif (castflag < 0):
                value = int(value)
            self.data_dictionary[newarray+i] = value
        self.ds -= 1
        self.data_stack[self.ds-1] = newarray
    def STEP_ARRAYCAT(self):
        '''
        LOFFSET ROFFSET TYPEFLAG (top)
        ->
        LOFFSET+ROFFSET (concatenation)
        '''
        self.ip += 1
        leftarray = self.data_stack[self.ds-3]
        rightarray = self.data_stack[self.ds-2]
        castflag = self.data_stack[self.ds-1]
        lcount = self.data_dictionary[leftarray-1]
        rcount = self.data_dictionary[rightarray-1]
        newarray = self.__helpAlloc__(lcount+rcount)
        for i in range(0, lcount):
            value = self.data_dictionary[leftarray+i]
            if (castflag > 0):
                value = float(value)
            elif (castflag < 0):
                value = int(value)
            self.data_dictionary[newarray+i] = value
        dstix = lcount
        for i in range(0, rcount):
            value = self.data_dictionary[rightarray+i]
            if (castflag > 0):
                value = float(value)
            elif (castflag < 0):
                value = int(value)
            self.data_dictionary[newarray+dstix] = value
            dstix += 1
        self.ds -= 2
        self.data_stack[self.ds-1] = newarray
    # STUDENT offsets into memory region, see comments for __helpAlloc__ below.
    __MEMHDR__ = 0      # Total size of the region, user & administrative data
    __MEMRFC__ = 1      # REFERENCECOUNT below
    __MEMLEN__ = 2      # Number of actual user array elements requested.
    __MEMPRV__ = 2      # PREVIOUS in doubly linked free list node
    __MEMNXT__ = 3      # NEXT in doubly linked free list node
    __MEMAPD__ = 3      # APplication Data is at some spot as __MEMNXT__.
    __MEMOVH__ = 4      # OVERHEAD: __MEMHDR__,__MEMRFC__,__MEMLEN__,FOOTER
    __MEMMINREQ__ = 1   # Minimum size of a user request or __MEMNXT__.
    __MEMMINTOT__ = __MEMOVH__ + __MEMMINREQ__
    def __helpAlloc__(self, amount):
        '''
        Allocate amount locations on the heap using either first fit or
        best fit allocation. Return the offset into the data dictionary
        where this contiguous storage resides. The returned index is to
        storage that can be used by the application program issuing
        STEP_ALLOC, i.e., it must not point to a header for the region
        owned by the memory manager. It points to the allocated region
        + __MEMAPD__ as defined for this class.
        '''
        # TODO STUDENT work goes below. Use the folliwng documentation.
        # MEMORY LAYOUT OF A REGION IN THE HEAP GIVEN BY THE CONSTANTS ABOVE:
        #
        # __MEMHDR__ | __MEMRFC__ | __MEMLEN__ or __MEMPRV__ |
        # __MEMNXT__ or __MEMAPD__ . . . (app or free space) | FOOTER
        #
        # First word in the heap is an index to free list, possibly None.
        # On the first call to __helpAlloc__ there will be no allocated
        # memory in the data_dictionary starting at self.start_of_heap.
        # You must grow data_dictionary AS NEEDED. Reuse memory off of the
        # free list when possible, and coalesce adjacent free regions.
        #
        # Each allocated or freed continguous region is layed out like this:
        # 0. __MEMHDR__
        #       WORDS-IN-REGION (this is the header), where WORDS-IN-REGION
        #       include all of the above administrative fields + space
        #       available for application use. It is overal size of the region.
        # 1. __MEMRFC__
        #       The REFERENCECOUNT, which is 0 for a free region. If this number
        #       goes < 0, there is a bug in generated code or the VM code.
        # 2. __MEMLEN__ or __MEMPRV__
        #       For an allocated region comes __MEMLEN__, which is the number
        #       of memory words actually requested by the STEP_ALLOC call.
        #       It may be less than the total words starting at __MEMAPD__,
        #       because your allocator should not split out and store on the
        #       free list regions that are too small to use. If that would
        #       happen, just allow some leftover space to reside at the tail
        #       end of the __MEMAPD__ section, after the alloc'd words and
        #       just before the FOOTER. __MEMLEN__ gives only the words
        #       requested by STEP_ALLOC; __MEMHDR__ gives total region size.
        #       __MEMLEN__ must always be >= 0. For allocating 0-length arrays
        #       of type any[], the compiler can invoke STEP_ALLOC to return
        #       the index of a singleton, interned, 0-element region.
        #       All requests for 0-elements share this singleton region.
        #       For an unallocated region __MEMPRV__ is the data_dictionary
        #       index of the *previous* free node in the doubly-linked free
        #       list, with value of None for the first node in the free list.
        # 3. __MEMNXT__ or __MEMAPD__
        #       For an unallocated region __MEMNXT__ is the data_dictionary
        #       index of the *next* free node in the doubly-linked free
        #       list, with value of None for the final node in the free list.
        #       For an allocated region __MEMAPD__ is the index of the first
        #       allocated word in memory. A minimum of __MEMLEN__ words
        #       are allocated, but there may be more if partitioning the region
        #       would lead to a subregion too small to use. See __MEMLEN__.
        # ... ADDITIONAL ALLOCATED OR ALLOC-ABLE WORDS COME AFTER __MEMAPD__.
        # N-1. WORDS-IN-REGION (this is the FOOTER). It has the same length-
        #       length-of-region contents as __MEMHDR__.
        # Thus the minimum size of a region is 5 locations, being:
        #   A) header, B) reference count, C) previous free region or
        #   application word count, D) next free region or first application
        #   word, E) footer. The intern'd 0-length region constructed by 
        #   __helpInitHeap__() is only 4 because it has no __MEMAPD__ and
        #   no __MEMNXT__.
        # Parson's free list is sorted by descending size of its regions.
        # I chose to implement best fit. Leave the next 2 lines intact:
        if (amount == 0):   # Return intern'd region that is never collected.
            return (self.start_of_heap + 1 + self.__MEMAPD__)
        # STUDENT CODE GOES BELOW:
        realamt = amount if (amount >= self.__MEMMINREQ__)      \
            else self.__MEMMINREQ__
        totalamt = realamt + self.__MEMOVH__
        nextfree = None
        previous = None
        nextfree = self.data_dictionary[self.start_of_heap]
        while (nextfree != None and self.data_dictionary[nextfree] >= totalamt):
            previous = nextfree ;
            nextfree = self.data_dictionary[nextfree+self.__MEMNXT__]
        if (previous != None):
            # There is a free list region that satisfies the request.
            region = previous
            self.__helpAllocGetFromFreelist__(region)
            available = self.data_dictionary[region]
            leftover = available - totalamt
            if leftover >= self.__MEMMINTOT__:
                # The leftover has to re-enter the free space
                orphan = region + totalamt
                self.data_dictionary[region] = totalamt         # header
                self.data_dictionary[orphan-1] = totalamt       # footer
                self.data_dictionary[orphan] = leftover         # header
                self.data_dictionary[orphan+leftover-1] = leftover # footer
                self.__helpAllocReturnToFreelist__(orphan)
            self.data_dictionary[region+self.__MEMRFC__] = 1
        else:
            # There is NO free list region that satisfies the request.
            region = len(self.data_dictionary)
            self.data_dictionary.extend([None for i in range(0,totalamt)])
            self.data_dictionary[region] = totalamt             # header
            self.data_dictionary[region+totalamt-1] = totalamt  # footer
            self.data_dictionary[region+self.__MEMRFC__] = 1
        self.data_dictionary[region+self.__MEMLEN__] = amount
        return (region+self.__MEMAPD__)
    def __helpRefcount__(self, offset, delta):
        '''
        Add delta to the reference count for the memory region at offset,
        and return the new reference count, which may be 0 for a negative
        delta. If it falls below 0, there is a bug in the compiler or VM.
        '''
        # Leave the next 3 lines intact.
        if offset == (self.start_of_heap + 1 + self.__MEMAPD__):
            # This is the 0-element interned region that is never collected.
            return (self.start_of_heap + 1 + self.__MEMRFC__)
        elif offset < self.start_of_heap:       # static storage
            return maxint
        # STUDENT CODE GOES BELOW:
        region = offset - self.__MEMAPD__
        oldcount = self.data_dictionary[region+self.__MEMRFC__]
        newcount = oldcount + delta
        if (newcount < 0):
            raise ValueError, "STEP_REFCNT drops below 0 for region "   \
                + str(offset) + ", reference count = " + str(newcount) + "."
        elif (newcount == 0):
            self.data_dictionary[region+self.__MEMRFC__] = 0
            self.data_dictionary[region+self.__MEMPRV__] = None
            self.data_dictionary[region+self.__MEMNXT__] = None
            newsize = self.data_dictionary[region]
            # This region now joins the free list. Coalesce!
            # Determine whether we can join it with a preceding or
            # following region. Check the following region first because it
            # then has to come out of the free list.
            neighbor = region + self.data_dictionary[region]
            if (neighbor < len(self.data_dictionary)                \
                    and self.data_dictionary[neighbor+self.__MEMRFC__] == 0):
                self.__helpAllocGetFromFreelist__(neighbor)
                newsize += self.data_dictionary[neighbor]
                self.data_dictionary[region] = newsize
                self.data_dictionary[region+newsize-1] = newsize
            # Done with the region after, now do the region before.
            footer = region - 1
            if footer > self.start_of_heap:
                neighbor = footer - self.data_dictionary[footer] + 1 # header
                if self.data_dictionary[neighbor+self.__MEMRFC__] == 0:
                    # Take the neighbor out of its free list, unless it
                    # is already at the correct spot.
                    region = neighbor
                    newsize += self.data_dictionary[region]
                    previous = self.data_dictionary[region+self.__MEMPRV__]
                    if (not (previous == None                            \
                            or self.data_dictionary[previous] >= newsize)):
                        # In this case we have to re-sort the grown region.
                        self.__helpAllocGetFromFreelist__(region)
                    self.data_dictionary[region] = newsize
                    self.data_dictionary[region+newsize-1] = newsize
            if self.data_dictionary[region+self.__MEMPRV__] == None         \
                    and self.data_dictionary[region+self.__MEMNXT__] == None \
                    and not self.data_dictionary[self.start_of_heap] == region:
                # There is no region before or after it on the free list,
                # and it is *not* the sole member of the free list, so add it
                # to the free list.
                self.__helpAllocReturnToFreelist__(region)
        else:       # newcount > 0
            self.data_dictionary[region+self.__MEMRFC__] = newcount
        return newcount
    def __helpInitHeap__(self):
        # Added Jan. 29 2012 for STEP_ALLOC, the memory manager adds a dummy
        # allocated array with 0-element capacity right after the pointer
        # to the start of the free list, and effectively gives it an
        # infinite reference count. STEP_ALLOC requests to allocate 0
        # words all return this region, and STEP_REFCNT to free it are ignored,
        # returns its maximal reference count without decrementing itelf.
        # The method is completed -- not student code to write.
        self.data_dictionary.extend([
            # This first entry is the pointer to the free list of regions.
            None,               # FREELIST: start of initial free list is empty
            # These remaining entries are 4 fields in the intern'd, 0-length
            # array that is used for any STEP_ALLOC request of 0-length.
            # It is never copied nor placed into the free list.
            # The reference count is never decremented.
            self.__MEMOVH__,    # __MEMHDR__: No alloc'd data or __MEMNXT__.
            maxint,             # __MEMRFC__: place-holding max reference count
            0,                  # __MEMLEN__: array length == 0
            self.__MEMOVH__])   # REGION FOOTER same as header
    def __helpAllocGetFromFreelist__(self, region):
        # region is assumed to be in the free list. Detach it.
        # __MEMPRV__, __MEMNXT__ and the start_of_heap are the only
        # fields used by this method. they are reset to None for the
        # region by this method.
        previous = self.data_dictionary[region+self.__MEMPRV__]
        nextfree = self.data_dictionary[region+self.__MEMNXT__]
        if previous != None:
            self.data_dictionary[previous+self.__MEMNXT__]            \
                = self.data_dictionary[region+self.__MEMNXT__]
        else:
            self.data_dictionary[self.start_of_heap]    \
                = self.data_dictionary[region+self.__MEMNXT__]
        if nextfree != None:
            self.data_dictionary[nextfree+self.__MEMPRV__]            \
                = self.data_dictionary[region+self.__MEMPRV__]
        self.data_dictionary[region+self.__MEMPRV__] = None
        self.data_dictionary[region+self.__MEMNXT__] = None
    def __helpAllocReturnToFreelist__(self, region):
        # region must not be on free list,
        # header & footer must give correct size.
        mysize = self.data_dictionary[region]
        self.data_dictionary[region+self.__MEMRFC__] = 0
        nextfree = self.data_dictionary[self.start_of_heap]
        previous = None
        while (nextfree != None                                 \
                and self.data_dictionary[nextfree] > mysize):
            previous = nextfree ;
            nextfree = self.data_dictionary[nextfree+self.__MEMNXT__]
        if (previous != None):
            self.data_dictionary[previous+self.__MEMNXT__] = region
        else:
            self.data_dictionary[self.start_of_heap] = region
        self.data_dictionary[region+self.__MEMPRV__] = previous
        self.data_dictionary[region+self.__MEMNXT__] = nextfree
        if (nextfree != None):
            self.data_dictionary[nextfree+self.__MEMPRV__] = region
    def __debugHeap__(self, outfile=stderr):
        '''
        This method is a helper that students can invoke to dump the
        heap to a file supplied in parameter outfile, by default sys.stderr.
        The dump occurs in two passes, a linear sweep over the heap, followed
        by a traversal of the free list.
        '''
        printer = PrettyPrinter(indent=4, width=80, stream=outfile)
        outfile.write('UNINTERPRETED DUMP OF THE ENTIRE DATA_DICTIONARY:\n')
        printer.pprint(self.data_dictionary)
        # This method is completed, and used for testing & debugging.
        if self.start_of_heap == len(self.data_dictionary):
            outfile.write("DEBUG HEAP: No heap allocated, "             \
                "size of data_dictionary = " + str(len(self.data_dictionary)) \
                    + '.\n')
            outfile.flush()
            return
        outfile.write("DEBUG HEAP: size of data_dictionary = "
            + str(len(self.data_dictionary)) + '.\n')
        outfile.write("DEBUG HEAP: free list pointer at location "           \
            + str(self.start_of_heap) + " = "                      \
                + str(self.data_dictionary[self.start_of_heap]) + '.\n')
        heap = self.start_of_heap + 1
        while heap > self.start_of_heap and heap < len(self.data_dictionary):
            if (self.data_dictionary[heap] < self.__MEMMINTOT__     \
                    and not heap == (self.start_of_heap + 1)):
                # The intern'd 0-element region violates this constraint.
                outfile.write("DEBUG HEAP Illegal region too small at " \
                    + str(heap) + ", region size = "                    \
                    + str(self.data_dictionary[heap]) + ", required = " \
                    + str(self.__MEMMINTOT__) + '.\n')
                outfile.flush()
                raise ValueError,                           \
                    "Illegal heap region too small, see heap dump."
            outfile.write("DEBUG HEAP @ " + str(heap) + ": HDR="        \
                + str(self.data_dictionary[heap]) + "|RFC="             \
                + str(self.data_dictionary[heap+self.__MEMRFC__]) + "|" \
                + str(self.data_dictionary[heap+self.__MEMLEN__]) + "|" \
                + str(self.data_dictionary[heap+self.__MEMAPD__]))
            after = heap + self.data_dictionary[heap]
            footer = after - 1
            if (footer <= self.start_of_heap                            \
                    or footer >= len(self.data_dictionary)):
                outfile.write("\nDEBUG HEAP Invalid FOOTER Location: "  \
                    + str(footer) + '.\n')
                outfile.flush()
                raise ValueError,                           \
                    "Illegal footer address, see heap dump."
            elif (self.data_dictionary[footer] != self.data_dictionary[heap]):
                outfile.write("\nDEBUG HEAP HEADER / FOOTER Mismatch: "  \
                    + str(heap) + ' holds ' + str(self.data_dictionary[heap]) \
                    +  ', ' + str(footer) + ' holds '               \
                        + str(self.data_dictionary[footer]))
                outfile.flush()
                raise ValueError,                           \
                    "Illegal header / footer mismatch, see heap dump."
            else:
                outfile.write("\nFOOTER@" + str(footer) + " = " \
                    + str(self.data_dictionary[footer]) + '.\n')
                outfile.flush()
            if self.data_dictionary[heap+self.__MEMRFC__] != 0:
                # dump cotents on the allocated ones but not the free ones
                for ii in range(0, self.data_dictionary[heap+self.__MEMLEN__]):
                    outfile.write('\t['+ str(ii) +'] = '        \
                        + str(self.data_dictionary[heap+self.__MEMAPD__+ii]) \
                            +'\n')
                outfile.flush()
            heap = after
        heap = self.data_dictionary[self.start_of_heap]
        while heap != None:
            if (heap <= self.start_of_heap                          \
                    or heap >= len(self.data_dictionary)):
                outfile.write("DEBUG FREE LIST INVALID ENTRY LOCATION: "    \
                    + str(heap) + '.\n')
                outfile.flush()
                raise ValueError,                           \
                    "Illegal free list address, see heap dump."
            outfile.write("DEBUG FREE LIST ENTRY @ " + str(heap) + ": HDR=" \
                + str(self.data_dictionary[heap]) + "|RFC="             \
                + str(self.data_dictionary[heap+self.__MEMRFC__]) + "|" \
                + str(self.data_dictionary[heap+self.__MEMPRV__]) + "|" \
                + str(self.data_dictionary[heap+self.__MEMNXT__]) + '.\n')
            if (self.data_dictionary[heap+self.__MEMRFC__] != 0):
                outfile.write("DEBUG FREE LIST ENTRY ERROR IN LAST ENTRY.\n");
                outfile.flush()
                raise ValueError,                           \
                    "Illegal free list entry, see heap dump."
            outfile.flush()
            heap = self.data_dictionary[heap+self.__MEMNXT__]
