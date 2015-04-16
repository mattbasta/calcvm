/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  v1:P|L v2:L --> (v1+v2):P
 *  (with top-of-dataStack to the right).
 *  Add an offset to an array pointer, leave the offset pointer on the stack.
 *  If the array reference is Long (in static storage), does Long addition,
 *  otherwise constructing an opaque pointer object with the offset.
**/
@Immutable
public class STEP_PADD extends StepOpCodeHelper implements StepOpCode {
    private final STEP_LADD ladder = new STEP_LADD();
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object value1 = dstack[ds-2];
        if (value1 instanceof Long) {
            ladder.eval(vm, context);
        } else {
            StepVM.HeapData ref = (StepVM.HeapData)(dstack[ds-2]);
            long value2 = ((Long)(dstack[ds-1])).longValue();
            dstack[ds-2] = vm.helpIndex(ref, (int)value2);
            vm.ds[context] -= 1 ;
            vm.ip[context] += 1 ;
        }
    }
}
