/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  valueToStore (see also in-line offset) --> (none)
 *  (with top-of-dataStack to the right).
 *  (The offset from the current FP at which to store is an in-line Long.)
**/
@Immutable
public class STEP_STORE_REGISTER
        extends StepOpCodeHelper implements StepOpCode {
    /**
     *  STEP_STORE_REGISTER takes an *in-line* Long, adds it to the current
     *  activation frame's FP, and stores the top of the data stack into
     *  that location in the stack frame. It is useful only for storing
     *  arguments and local variables that are in the innermost lexical scope.
     *  Accessing non-local variables from surrounding lexical scopes still
     *  requires iterating through static and then adding an offset to the
     *  correct one. "Registers" are for genuinely local variables and
     *  arguments in the current frame.
    **/
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int ip = vm.ip[context];
        int offset = (int)(((Long)(vm.programMemory[ip+1])).longValue());
        Object value = dstack[ds-1];
        dstack[vm.fp[context] + offset] = value ;
        vm.ds[context] -= 1 ;
        vm.ip[context] += 2 ;
    }
}
