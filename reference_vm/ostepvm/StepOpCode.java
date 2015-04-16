/*
    StepOpCode.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  StepOpCode is an interface inherited by all op code classes for
 *  StepVM. Objects of StepOpCode should be stateless, i.e., immutable.
 *  @author Dr. Dale Parson
**/
@Immutable
public interface StepOpCode {
    /**
     *  Interpret this op code in the VM, typically modify the 'ip' register.
     *  An op code that encounters an invalid instruction or a STEP_PAUSE
     *  StepOpCode objects are intended to be stateless.
     *  A StepOpCode must grow the dataStack and controlStack for its
     *  hardware thread (context) if needed by the instruction.
     *  StepOpCode will throw a StepRuntimeException or other RuntimeException.
     *  @param vm is the virtual machine being run.
     *  @param context is the hardware thread running this op code.
     *  Only one Java thread at a time is allowed to run in a VM context.
     *
    **/
    public void eval(StepVM vm, int context);
}
