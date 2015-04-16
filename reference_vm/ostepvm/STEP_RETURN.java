/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  CONTROL STACK : CALLER_FP CALLER_RETURNADDRESS --> (nothing)
 *  (with top-of-dataStack to the right).
**/
public class STEP_RETURN extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        int [] cstack = vm.controlStack[context] ;
        int cs = vm.cs[context];
        vm.ip[context] = cstack[cs-1];      // return address
        vm.fp[context] = cstack[cs-2];      // caller's FP
        vm.cs[context] -= 2 ;
    }
}
