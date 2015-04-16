/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x --> (none)
 *  (with top-of-dataStack to the right).
**/
public class STEP_DROP extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
