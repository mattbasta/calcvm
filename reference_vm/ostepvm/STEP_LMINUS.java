/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  v:L --> (-v):L
 *  (with top-of-dataStack to the right).
**/
public class STEP_LMINUS extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-1] = new Long(-value);
        vm.ip[context] += 1 ;
    }
}
