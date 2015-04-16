/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  arrayref:OPAQUEPTR refcountDelta:L --> (nothing pushed to stack)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_REFCNT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        if (dstack[ds-2] instanceof StepVM.HeapData) {
            // Otherwise it should be a Long reference to static storage.
            StepVM.HeapData region = ((StepVM.HeapData)(dstack[ds-2]));
            long delta = ((Long)(dstack[ds-1])).longValue();
            if (region.offset > 0) {
                throw new StepVMMemoryException("STEP_REFCNT ERROR: "
                    + "attempt to decrement an array offset: "
                    + region.toString(),vm);
            }
            region.addToRefCount(delta);
        }
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
