/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  value address:L:P --> (none)
 *  (with top-of-dataStack to the right).
 *  address may be a Long index into static memory in dataMemory or
 *  an opaque pointer into the heap.
**/
public class STEP_STORE extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object address = dstack[ds-1];
        Object value = dstack[ds-2];
        if (address instanceof Long) {
            int staticAddress = (int)((Long)address).longValue();
            vm.dataMemory[staticAddress] = value ;
        } else {
            StepVM.HeapData haddr = (StepVM.HeapData) address ;
            haddr.appData[haddr.offset] = value ;
        }
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
