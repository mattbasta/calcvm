/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  x --> (none)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_DROP extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
