/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  x y --> y x
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_SWAP extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object tmp = dstack[ds-1];
        dstack[ds-1] = dstack[ds-2];
        dstack[ds-2] = tmp ;
        vm.ip[context] += 1 ;
    }
}
