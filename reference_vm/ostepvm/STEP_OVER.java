/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  data1 data2 --> data1 data2 data1
 *  (with top-of-dataStack to the right).
**/
public class STEP_OVER extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 1, 000);
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        dstack[ds] = dstack[ds-2];
        vm.ds[context] += 1 ;
        vm.ip[context] += 1 ;
    }
}
