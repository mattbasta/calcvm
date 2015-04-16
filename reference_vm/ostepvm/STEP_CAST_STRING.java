/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  value:? --> value:S
 *  (with top-of-dataStack to the right).
**/
public class STEP_CAST_STRING extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object value = dstack[ds-1];
        if (value != null && !(value instanceof String)) {
            value = value.toString();
        }
        dstack[ds-1] = value ;
        vm.ip[context] += 1 ;
    }
}
