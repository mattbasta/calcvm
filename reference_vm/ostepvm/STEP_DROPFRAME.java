/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  bottomOffset:L topOffset:L --> (none)
 *  (with top-of-dataStack to the right).
**/
public class STEP_DROPFRAME extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int bottom = (int)((Long)dstack[ds-2]).longValue();
        int top = (int)((Long)dstack[ds-1]).longValue();
        vm.ds[context] -= 2 ;
        int count = top - bottom + 1 ;
        int originalCount = count ;
        int beyond = top + 1 ;
        while (count > 0 && beyond < vm.ds[context]) {
            dstack[bottom] = dstack[beyond];
            bottom++ ;
            beyond++ ;
            count-- ;
        }
        vm.ds[context] -= originalCount ;
        vm.ip[context] += 1 ;
    }
}
