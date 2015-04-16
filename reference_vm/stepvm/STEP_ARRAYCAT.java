/*  Implementation of a StepVM op code class. */

package newvm3.stepvm ;
import java.util.Arrays ;
import net.jcip.annotations.* ;

/**
 *  larrayref:P|L rarrayref:P|L typeflag:L --> newarrayref:P
 *  (with top-of-dataStack to the right).
 *  typeflag is >0 for Double, <0 for Long, 0 for none.
 *  If either incoming array reference is a Long, it is copied from
 *  dataMemory (static data). If either is an opaque HeapData object,
 *  it is copied from the heap. The result is on the heap.
**/
@Immutable
public class STEP_ARRAYCAT extends StepOpCodeHelper implements StepOpCode {
    public void eval(StepVM vm, int context) {
        Object [] dstack = vm.dataStack[context] ;
        int ds = vm.ds[context];
        Object [] larray = null, rarray = null ;
        int lindex = 0, llen = 0, rindex = 0, rlen = 0 ;
        Object laddress = dstack[ds-3];
        if (laddress instanceof Long) {
            int staticAddress = (int)((Long)laddress).longValue();
            larray = vm.dataMemory ;
            lindex = staticAddress ;
            llen = (int)((Long)vm.dataMemory[staticAddress-1]).longValue();;
        } else {
            StepVM.HeapData haddr = (StepVM.HeapData) laddress ;
            if (haddr.offset > 0) {
                throw new StepVMMemoryException("STEP_ARRAYCAT ERROR: "
                    + "attempt to use an array offset: "
                    + haddr.toString(), vm);
            }
            larray = haddr.appData ;
            lindex = 0 ;
            llen = haddr.appData.length ;
        }
        Object raddress = dstack[ds-2];
        if (raddress instanceof Long) {
            int staticAddress = (int)((Long)raddress).longValue();
            rarray = vm.dataMemory ;
            rindex = staticAddress ;
            rlen = (int)((Long)vm.dataMemory[staticAddress-1]).longValue();;
        } else {
            StepVM.HeapData haddr = (StepVM.HeapData) raddress ;
            if (haddr.offset > 0) {
                throw new StepVMMemoryException("STEP_ARRAYCAT ERROR: "
                    + "attempt to use an array offset: "
                    + haddr.toString(), vm);
            }
            rarray = haddr.appData ;
            rindex = 0 ;
            rlen = haddr.appData.length ;
        }
        long typeflag = ((Long)(dstack[ds-1])).longValue();
        Object [] newmem = new Object [ llen+rlen ];
        int dst = 0 ;
        for (int i = 0 ; i < llen ; i++, dst++) {
            newmem[dst] = larray[lindex+i] ;
        }
        for (int i = 0 ; i < rlen ; i++, dst++) {
            newmem[dst] = rarray[rindex+i] ;
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
                            + " to a Double: " + newmem[i].toString(), vm);
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
                            + " to a Long: "+ newmem[i].toString(), vm);
                    }
                }
            }
        }
        dstack[ds-3] = vm.helpAlloc(newmem);
        vm.ds[context] -= 2 ;
        vm.ip[context] += 1 ;
    }
}
