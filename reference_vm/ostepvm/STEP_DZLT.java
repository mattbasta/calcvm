/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x:D --> (x < 0):L
 *  (with top-of-dataStack to the right).
**/
public class STEP_DZLT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        double value = ((Double)(dstack[ds-1])).doubleValue();
        dstack[ds-1] = new Double((value < 0.0) ? 1L : 0L);
        vm.ip[context] += 1 ;
    }
}
