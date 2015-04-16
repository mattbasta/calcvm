/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x:D y:D --> (x < y):L
 *  (with top-of-dataStack to the right).
**/
public class STEP_DLT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        double value1 = ((Double)(dstack[ds-2])).doubleValue();
        double value2 = ((Double)(dstack[ds-1])).doubleValue();
        dstack[ds-2] = new Long((value1 < value2) ? 1L : 0L);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
