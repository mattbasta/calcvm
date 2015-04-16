/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  testvalue:L --> (none)
 *  (with top-of-dataStack to the right).
 *  Conditional GOTO if 0 on data stack.
**/
@Immutable
public class STEP_GOTO0 extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        long value = ((Long)(dstack[ds-1])).longValue();
        vm.ds[context] -= 1 ;
        if (value == 0L) {
            int address = (int)(((Long)
                (vm.programMemory[vm.ip[context]+1])).longValue());
            vm.ip[context] = address ; // make the jump
        } else {
            vm.ip[context] += 2 ;
        }
    }
}
