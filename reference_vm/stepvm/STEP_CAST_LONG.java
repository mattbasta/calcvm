/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  value:? --> value:L
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_CAST_LONG extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object value = dstack[ds-1];
        if (value != null && !(value instanceof Long)) {
            if (value instanceof Double) {
                value = new Long(((Double)(value)).longValue());
            } else if (value instanceof String) {
                value = new Long(value.toString());
            } else {
                throw new StepVMMemoryException("STEP_CAST_DOUBLE ERROR: "
                    + "attempt to cast an element type of "
                    + value.getClass().toString()
                    + " to a Double: " + value.toString(), vm);
            }
        }
        dstack[ds-1] = value ;
        vm.ip[context] += 1 ;
    }
}
