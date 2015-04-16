/*  Implementation of a StemVM op code class. */

package newvm3.stepvm ;
import java.util.Arrays ;
import net.jcip.annotations.* ;

@Immutable
/**
 *  larrayref:OPAQUEPTR rarrayref:OPAQUEPTR typeflag:L --> newarrayref:OPAQUEPTR
 *  (with top-of-dataStack to the right).
 *  typeflag is >0 for Double, <0 for Long, 0 for none.
**/
public class STEP_ARRAYCAT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        StepVM.HeapData lregion = ((StepVM.HeapData)(dstack[ds-3]));
        StepVM.HeapData rregion = ((StepVM.HeapData)(dstack[ds-2]));
        long typeflag = ((Long)(dstack[ds-1])).longValue();
        if (lregion.offset != -1) {
            throw new StepVMMemoryException("STEP_ARRAYCAT ERROR: "
                + "attempt to use an array offset: "
                + lregion.toString());
        }
        if (rregion.offset != -1) {
            throw new StepVMMemoryException("STEP_ARRAYCAT ERROR: "
                + "attempt to use an array offset: "
                + rregion.toString());
        }
        Object [] newmem = Arrays.copyOf(lregion.appData,
            lregion.appData.length + rregion.appData.length);
        for (int from = 0, to = lregion.appData.length ;
                from < rregion.appData.length ; from++, to++) {
            newmem[to] = rregion.appData[from];
        }
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
                            + " to a Double: "
                            + ((i < lregion.appData.length)
                                ? lregion.toString() : rregion.toString()));
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
                            + " to a Long: "
                            + ((i < lregion.appData.length)
                                ? lregion.toString() : rregion.toString()));
                    }
                }
            }
        }
        dstack[ds-3] = vm.helpAlloc(newmem);
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
