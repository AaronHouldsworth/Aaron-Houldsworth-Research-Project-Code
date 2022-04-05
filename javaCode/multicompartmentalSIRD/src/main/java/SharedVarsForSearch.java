public class SharedVarsForSearch {
    volatile boolean globalFound;
    volatile int globalPointer;
    volatile double globalSum;
    
    SharedVarsForSearch(){
        globalFound = false;
        globalPointer = 0;
        globalSum = 0;
    }
    
}
