/*
    StepRuntimeException.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
/**
 *  StepRuntimeException is the exception class base class for StepVM. It
 *  derives from java.lang.RuntimeException because it represents a run-time
 *  exception in compiler-generated VM code.
 *  @author Dr. Dale Parson
**/
public class StepRuntimeException extends RuntimeException {
    /** Construct an exception with a message. **/
    public StepRuntimeException(String message) {
        super(message);
    }
    /** Construct an exception with a message and a cause. **/
    public StepRuntimeException(String message, Throwable cause) {
        super(message, cause);
    }
}
