/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  valueToStore OffsetFromBottomOfStack:L --> (none)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_STORE_STACK extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int offset = (int)(((Long)(dstack[ds-1])).longValue());
        Object value = dstack[ds-2];
        dstack[offset] = value;
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
