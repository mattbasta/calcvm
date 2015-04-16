/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  address:L:P --> numberOfApplicationElements:L
 *  (with top-of-dataStack to the right).
 *  address may be a Long index into static memory in dataMemory or
 *  an opaque pointer into the heap.
**/
@Immutable
public class STEP_ARRAYCOUNT extends StepOpCodeHelper implements StepOpCode {
    /**
     *  STEP_ARRAYCOUNT fetches the application element count associated
     *  with an array reference, replacing the reference with the count on
     *  the data stack. It does not affect the reference count of the
     *  array reference in any way.
    **/
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object address = dstack[ds-1];
        if (address instanceof Long) {
            int staticAddress = (int)((Long)address).longValue();
            dstack[ds-1] = vm.dataMemory[staticAddress-1];
        } else {
            StepVM.HeapData haddr = (StepVM.HeapData) address ;
            dstack[ds-1] = new Long(haddr.appData.length);
        }
        vm.ip[context] += 1 ;
    }
}
