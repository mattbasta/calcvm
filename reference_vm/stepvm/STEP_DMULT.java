/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  v1:D v2:D --> (v1*v2):D
 *  (with top-of-dataStack to the right).
**/
@Immutable
public class STEP_DMULT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        double value1 = ((Double)(dstack[ds-2])).doubleValue();
        double value2 = ((Double)(dstack[ds-1])).doubleValue();
        dstack[ds-2] = new Double(value1*value2);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
