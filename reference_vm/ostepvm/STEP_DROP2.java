/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  x y --> (none)
 *  (with top-of-dataStack to the right).
**/
public class STEP_DROP2 extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
