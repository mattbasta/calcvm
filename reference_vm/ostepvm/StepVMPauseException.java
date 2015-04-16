/*
    StepVMPauseException.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
/**
 *  StepVMPauseException is the exception class thown by the StepVM when
 *  a STEP_PAUSE op code is executed.
 *  @author Dr. Dale Parson
**/
public class StepVMPauseException extends StepRuntimeException {
    /** Construct an exception with a message. **/
    public StepVMPauseException(String message) {
        super(message);
    }
    /** Construct an exception with a message and a cause. **/
    public StepVMPauseException(String message, Throwable cause) {
        super(message, cause);
    }
}
