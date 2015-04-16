/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x:L y:L --> (x != y):L
 *  (with top-of-dataStack to the right).
**/
public class STEP_LNEQ extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value1 = ((Long)(dstack[ds-2])).longValue();
        long value2 = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-2] = new Long((value1 != value2) ? 1L : 0L);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
