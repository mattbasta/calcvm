/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  v1:L v2:L --> (v1^v2):L
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_LBITXOR extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value1 = ((Long)(dstack[ds-2])).longValue();
        long value2 = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-2] = new Long(value1^value2);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
