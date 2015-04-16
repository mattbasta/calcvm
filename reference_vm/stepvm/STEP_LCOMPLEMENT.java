/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  v:L --> (~v):L
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_LCOMPLEMENT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-1] = new Long(~value);
        vm.ip[context] += 1 ;
    }
}
