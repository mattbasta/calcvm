/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import java.util.Arrays ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  arrayref:OPAQUEPTR typeflag:L --> newarrayref:OPAQUEPTR
 *  (with top-of-dataStack to the right).
 *  typeflag is >0 for Double, <0 for Long, 0 for none.
**/
public class STEP_ARRAYCPY extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        StepVM.HeapData region = ((StepVM.HeapData)(dstack[ds-2]));
        long typeflag = ((Long)(dstack[ds-1])).longValue();
        if (region.offset != -1) {
            throw new StepVMMemoryException("STEP_ARRAYCPY ERROR: "
                + "attempt to copy an array offset: "
                + region.toString());
        }
        Object [] newmem = Arrays.copyOf(region.appData, region.appData.length);
        if (typeflag > 0) {
            for (int i = 0 ; i < newmem.length ; i++) {
                if (newmem[i] != null && !(newmem[i] instanceof Double)) {
                    if (newmem[i] instanceof Long) {
                        newmem[i] = new Double(((Long)
                            (newmem[i])).doubleValue());
                    } else if (newmem[i] instanceof String) {
                        newmem[i] = new Double(newmem[i].toString());
                    } else {
                        throw new StepVMMemoryException("STEP_ARRAYCPY ERROR: "
                            + "attempt to cast an element type of "
                            + newmem[i].getClass().toString()
                            + " to a Double: " + region.toString());
                    }
                }
            }
        } else if (typeflag < 0) {
            for (int i = 0 ; i < newmem.length ; i++) {
                if (newmem[i] != null && !(newmem[i] instanceof Long)) {
                    if (newmem[i] instanceof Double) {
                        newmem[i] = new Long(((Double)
                            (newmem[i])).longValue());
                    } else if (newmem[i] instanceof String) {
                        newmem[i] = new Long(newmem[i].toString());
                    } else {
                        throw new StepVMMemoryException("STEP_ARRAYCPY ERROR: "
                            + "attempt to cast an element type of "
                            + newmem[i].getClass().toString()
                            + " to a Long: " + region.toString());
                    }
                }
            }
        }
        dstack[ds-2] = vm.helpAlloc(newmem);
        vm.ds[context] -= 1 ;
        vm.ip[context] += 1 ;
    }
}
