/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  (none) --> (none)
 *  (with top-of-dataStack to the right).
 *  Prints a newline to System.out
**/
@Immutable
public class STEP_CRLF extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        System.out.println();
        vm.ip[context] += 1 ;
    }
}
