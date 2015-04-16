/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x --> x x x
 *  (with top-of-dataStack to the right).
**/
public class STEP_DUP2 extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 2, 000);
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        dstack[ds] = dstack[ds-1];
        dstack[ds+1] = dstack[ds-1];
        vm.ds[context] += 2 ;
        vm.ip[context] += 1 ;
    }
}
