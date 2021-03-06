/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  Nitems N --> (none)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_DROPN extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int N = (int)((Long)dstack[ds-1]).longValue();
        vm.ds[context] -= (N + 1);
        vm.ip[context] += 1 ;
    }
}
