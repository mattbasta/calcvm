/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  --> dataFromInlineOperand
 *  (with top-of-dataStack to the right).
**/
public class STEP_CONST extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 1, 000);
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int ip = vm.ip[context];
        dstack[ds] = vm.programMemory[ip+1];
        vm.ds[context] += 1 ;
        vm.ip[context] += 2 ;
    }
}
