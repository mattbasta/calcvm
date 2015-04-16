/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  OffsetFromBottomOfStack:L --> CopyOfItsValue
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_FETCH_STACK extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int offset = (int)(((Long)(dstack[ds-1])).longValue());
        dstack[ds-1] = dstack[offset];
        vm.ip[context] += 1 ;
    }
}
