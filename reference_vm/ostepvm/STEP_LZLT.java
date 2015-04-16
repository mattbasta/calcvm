/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x:L --> (x < 0):L
 *  (with top-of-dataStack to the right).
**/
public class STEP_LZLT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-1] = new Long((value < 0L) ? 1L : 0L);
        vm.ip[context] += 1 ;
    }
}
