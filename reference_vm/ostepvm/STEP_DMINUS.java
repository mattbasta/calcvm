/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  v:D --> (-v):D
 *  (with top-of-dataStack to the right).
**/
public class STEP_DMINUS extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        double value = ((Double)(dstack[ds-1])).doubleValue();
        dstack[ds-1] = new Double(-value);
        vm.ip[context] += 1 ;
    }
}
