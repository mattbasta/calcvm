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
    private volatile StepVM vm ;
    /**
     *  Construct an exception with a message.
     *  @param message is the getMessage() String.
     *  @param vm is the fully constructed StepVM object throwing the
     *  exception, use null if thrown outside of any VM context.
    **/
    public StepRuntimeException(String message, StepVM vm) {
        super(message);
        this.vm = vm ;
    }
    /**
     *  Construct an exception with a message and a cause.
     *  @param message is the getMessage() String.
     *  @param cause is any underlying cause such as an invalid type cast.
     *  @param vm is the fully constructed StepVM object throwing the
    **/
    public StepRuntimeException(String message, Throwable cause,
            StepVM vm) {
        super(message, cause);
        this.vm = vm ;
    }
    /** Retrieve the SteVM object throwing the exception, may be null. **/
    public StepVM getVM() {
        return vm ;
    }
    /**
     *  Set the VM throwing throwing this exception.
     *  This method if the exception constructor does not have access to the
     *  VM reference. The exception can be caught by the VM and then
     *  re-thrown after setVM().
     *  @param vm is the StepVM causing the exception, must be non-null.
    **/
    public void setVM(StepVM vm) {
        this.vm = vm ;
    }
}
