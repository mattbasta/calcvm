/*
    StepOpCodeHelper.java
    New STack-based Emulated Processor (STEP) for Compiler Design II,
    Spring 2012, D. Parson. See step.pdf and vm.py.txt for documentation
    on the C++ and Python predecessors to this VM, including documentation
    on its op codes and their effects on the data stack and registers.
*/

package newvm3.stepvm ;
import java.util.Arrays ;
import net.jcip.annotations.* ;

/**
 *  StepOpCodeHelper is a helper class for op codes that implements helper
 *  methods to ensure adequate size of the data stack and controk stack
 *  for an op code.
 *  Objects of StepOpCode should be stateless, i.e., immutable.
 *  @author Dr. Dale Parson
**/
@Immutable
public abstract class StepOpCodeHelper implements StepOpCode {
    /**
     *  Verify that the dataStack and controlStack are big enough to complete
     *  this op code, growing them if necessary.
     *  @param vm is the virtual machine being run.
     *  @param context is the hardware thread running this op code.
     *  Only one Java thread at a time is allowed to run in a VM context.
     *  @param dataStackGrowth is the additional data stack space required
     *  for this instruction, ignored if it is <= 0.
     *  @param controlStackGrowth is the additional control stack space required
     *  for this instruction, ignored if it is <= 0.
    **/
    protected void verifyStacks(StepVM vm, int context,
        int dataStackGrowth, int controlStackGrowth) {
        if (dataStackGrowth > 0 && (vm.ds[context] + dataStackGrowth)
                >= vm.dataStack[context].length) {
            int growsize = (dataStackGrowth >= StepVM.DATASTACKGROWSIZE)
                ? dataStackGrowth : StepVM.DATASTACKGROWSIZE ;
            vm.dataStack[context] = Arrays.copyOf(vm.dataStack[context],
                vm.dataStack[context].length + growsize);
        }
        if (controlStackGrowth > 0 && (vm.cs[context] + controlStackGrowth)
                >= vm.controlStack[context].length) {
            int growsize = (controlStackGrowth >= StepVM.CTRLSTACKGROWSIZE)
                ? controlStackGrowth : StepVM.CTRLSTACKGROWSIZE ;
            vm.controlStack[context] = Arrays.copyOf(vm.controlStack[context],
                vm.controlStack[context].length + growsize);
        }
    }
}
