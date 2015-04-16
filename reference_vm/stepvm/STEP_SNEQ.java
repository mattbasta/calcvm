/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  x:S y:S --> (x != y):L
 *  (with top-of-dataStack to the right).
 *  Return 1L on success, 0L on predicate test failed.
**/
@Immutable
public class STEP_SNEQ extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        String value1 = ((String)(dstack[ds-2]));
        String value2 = ((String)(dstack[ds-1]));
        dstack[ds-2] = new Long(value1.equals(value2) ? 0L : 1L);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
