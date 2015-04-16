/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  v1:S v2:S --> (v1+v2):S
 *  String concatenation (with top-of-dataStack to the right).
**/
public class STEP_SADD extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        StringBuilder value = new StringBuilder((String)(dstack[ds-2]));
        value.append((String)(dstack[ds-1]));
        dstack[ds-2] = value.toString();
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
