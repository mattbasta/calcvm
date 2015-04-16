/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

/**
 *  (nothing -- operand is in-line in program memory)  --> CopyOfLocalVariable
 *  (In-line datum is offset to add to current frame's FP.)
**/
@Immutable
public class STEP_FETCH_REGISTER
        extends StepOpCodeHelper implements StepOpCode {
    /**
     *  STEP_FETCH_REGISTER takes an *in-line* Long, adds it to the current
     *  activation frame's FP, and fetches that location onto the stack frame.
     *  It is useful only for fetching arguments and local variables that
     *  are in the innermost lexical scope. Accessing non-local variables from
     *  surrounding lexical scopes still requires iterating through static
     *  and then adding an offset to the correct one. "Registers" are for
     *  genuinely local variables and arguments in the current frame.
    **/
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 1, 000);
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        int ip = vm.ip[context];
        int offset = (int)(((Long)(vm.programMemory[ip+1])).longValue());
        dstack[ds] = dstack[vm.fp[context] + offset];
        vm.ds[context] += 1 ;
        vm.ip[context] += 2 ;
    }
}
