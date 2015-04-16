/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  arrayref:OPAQUEPTR refcountDelta:L --> (nothing pushed to stack)
 *  (with top-of-dataStack to the right).
**/
public class STEP_REFCNT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        StepVM.HeapData region = ((StepVM.HeapData)(dstack[ds-2]));
        long delta = ((Long)(dstack[ds-1])).longValue();
        if (region.offset != -1) {
            throw new StepVMMemoryException("STEP_REFCNT ERROR: "
                + "attempt to decrement an array offset: "
                + region.toString());
        }
        region.addToRefCount(delta);
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
