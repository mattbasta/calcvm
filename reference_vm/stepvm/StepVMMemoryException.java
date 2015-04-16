/*
    StepVMMemoryException.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
/**
 *  StepVMMemoryException is the exception class thown by the StepVM when
 *  a run-time memory access error occurs.
 *  @author Dr. Dale Parson
**/
public class StepVMMemoryException extends StepRuntimeException {
    /** Construct an exception with a message. **/
    public StepVMMemoryException(String message, StepVM vm) {
        super(message, vm);
    }
    /** Construct an exception with a message and a cause. **/
    public StepVMMemoryException(String message, Throwable cause, StepVM vm) {
        super(message, cause, vm);
    }
}
