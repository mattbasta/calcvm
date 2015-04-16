/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  Object --> (none)
 *  (with top-of-dataStack to the right).
 *  Object is printed to System.out with no newline.
**/
@Immutable
public class STEP_PRINT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object data = dstack[ds-1];
        System.out.print(data.toString());
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
