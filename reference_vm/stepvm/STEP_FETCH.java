/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  address:L:P --> data
 *  (with top-of-dataStack to the right).
 *  address may be a Long index into static memory in dataMemory or
 *  an opaque pointer into the heap.
**/
@Immutable
public class STEP_FETCH extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object address = dstack[ds-1];
        if (address instanceof Long) {
            int staticAddress = (int)((Long)address).longValue();
            dstack[ds-1] = vm.dataMemory[staticAddress];
        } else {
            StepVM.HeapData haddr = (StepVM.HeapData) address ;
            dstack[ds-1] = haddr.appData[haddr.offset];
        }
        vm.ip[context] += 1 ;
    }
}
