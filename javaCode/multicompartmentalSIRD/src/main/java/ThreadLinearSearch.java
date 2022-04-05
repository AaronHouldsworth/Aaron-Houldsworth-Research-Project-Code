
public class ThreadLinearSearch implements Runnable {
    
    double[] searchArray;
    int pointer;
    int pointerAugment;
    double target;
    double total;
    double preIndex;
    int maxIndex;
    SharedVarsForSearch sharedVar;
    
    ThreadLinearSearch(SharedVarsForSearch variable,double[] newArray, double newTarget, double newPreIndex,int newAugment){
        sharedVar = variable;
        this.searchArray = newArray;
        maxIndex = newArray.length;
        this.target = newTarget;
        this.preIndex = newPreIndex;
        this.pointerAugment = newAugment;
    }
    
    
    public void run(){
        
        double currentTotal = preIndex;
        int currentIndex = 0;
        
        
        while (!(sharedVar.globalFound) && currentIndex < maxIndex){
            
            if ((currentTotal<target) && (target<=currentTotal+searchArray[currentIndex])){
                sharedVar.globalFound = true;
                sharedVar.globalPointer = currentIndex+pointerAugment;
                sharedVar.globalSum = currentTotal;
            }else{
                currentTotal = currentTotal+searchArray[currentIndex];
                currentIndex = currentIndex+1;
            }
                        
        }
        
    }
    

}
