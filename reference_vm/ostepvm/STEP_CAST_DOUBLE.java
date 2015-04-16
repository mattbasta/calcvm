/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  value:? --> value:D
 *  (with top-of-dataStack to the right).
**/
public class STEP_CAST_DOUBLE extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object value = dstack[ds-1];
        if (value != null && !(value instanceof Double)) {
            if (value instanceof Long) {
                value = new Double(((Long)(value)).doubleValue());
            } else if (value instanceof String) {
                value = new Double(value.toString());
            } else {
                throw new StepVMMemoryException("STEP_CAST_DOUBLE ERROR: "
                    + "attempt to cast an element type of "
                    + value.getClass().toString()
                    + " to a Double: " + value.toString());
            }
        }
        dstack[ds-1] = value ;
        vm.ip[context] += 1 ;
    }
}
