/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  value:L --> absoluteValueOf(value:L)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_LABS extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        if (value < 0L) {
            dstack[ds-1] = new Long(-value);
        }
        vm.ip[context] += 1 ;
    }
}
