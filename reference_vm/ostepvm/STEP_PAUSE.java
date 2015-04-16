/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  (none) --> (none)
 *  (with top-of-dataStack to the right).
 *  Throws StepVMPauseException after advancing ip.
**/
public class STEP_PAUSE extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        int ip = vm.ip[context] ;
        vm.ip[context] += 1 ;
        throw new StepVMPauseException(
            "VM STEP_PAUSE, ip transitioning from " + ip + " to " + (ip+1));
    }
}
