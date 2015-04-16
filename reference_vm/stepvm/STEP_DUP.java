/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  x --> x x
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_DUP extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 1, 000);
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        dstack[ds] = dstack[ds-1];
        vm.ds[context] += 1 ;
        vm.ip[context] += 1 ;
    }
}
