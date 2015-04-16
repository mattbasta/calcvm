/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  (none) --> (none)
 *  (with top-of-dataStack to the right).
 *  Jumps to address in in-line data.
**/
public class STEP_GOTO extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        int address = (int)(((Long)
            (vm.programMemory[vm.ip[context]+1])).longValue());
        vm.ip[context] = address ; // make the jump
    }
}
