/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  CONTROL STACK : (nothing) --> CALLER_FP CALLER_RETURNADDRESS
 *  (with top-of-dataStack to the right).
**/
public class STEP_CALL_SECONDARY extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        verifyStacks(vm, context, 0, 2);
        int [] cstack = vm.controlStack[context] ;
        int cs = vm.cs[context];
        int ip = vm.ip[context];
        cstack[cs] = vm.fp[context];    // push frame pointer
        cstack[cs+1] = ip + 2 ;         // push return address
        vm.cs[context] += 2 ;
        vm.fp[context] = vm.ds[context] ;
        int address = (int)(((Long)(vm.programMemory[ip+1])).longValue());
        vm.ip[context] = address ; // make the call
    }
}
