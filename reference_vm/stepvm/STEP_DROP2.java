/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  x y --> (none)
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_DROP2 extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
