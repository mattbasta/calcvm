/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  arraysize:L --> arrayref:OPAQUEPTR
 *  (with top-of-dataStack to the right).
 *  The OPAQUEPTR can be added to Long offsets, fetch and stored in the heap.
**/
public class STEP_ALLOC extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        dstack[ds-1] = vm.helpAlloc((int)value);
        vm.ip[context] += 1 ;
    }
}
