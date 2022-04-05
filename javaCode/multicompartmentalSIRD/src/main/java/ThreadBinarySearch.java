import java.lang.Math;


public class ThreadBinarySearch implements Runnable {
    
    double[] searchArray;
    int pointer;
    int pointerAugment;
    double target;
    double total;
    double preIndex;
    int maxIndex;
    SharedVarsForSearch sharedVar;
    
    ThreadBinarySearch(SharedVarsForSearch variable,double[] newArray, double newTarget, double newPreIndex,int newAugment){
        sharedVar = variable;
        this.searchArray = newArray;
        maxIndex = newArray.length;
        this.target = newTarget;
        this.preIndex = newPreIndex;
        this.pointerAugment = newAugment;
    }
    
    
    public void run(){
        
        int noItems = searchArray.length;   
        pointer = (int) (Math.round(noItems/2));
        
        int lowIndex = 0;
        int highIndex = noItems-1;

        Boolean keepSearching = true;
        
        System.out.println("target");
        System.out.println(target);
        System.out.println("preIndex");
        System.out.println(preIndex);
        System.out.println("SearchArray[0]");
        System.out.println(searchArray[0]);
        
        if ((preIndex < target) && (target <= searchArray[0])){
            sharedVar.globalFound = true;
            sharedVar.globalPointer = pointerAugment;
            System.out.println("here1");
            System.out.println(pointerAugment);
        }

        while (!(sharedVar.globalFound) && keepSearching){
            System.out.println(pointer);
            System.out.println(target);
            for (double item : searchArray){
                System.out.print(item);
                System.out.print("|");
            }
            System.out.println(preIndex);
            System.out.println("");    
                
            if (pointer==0){
                if ((preIndex < target) && (target <= searchArray[0])){
                    sharedVar.globalFound = true;
                    sharedVar.globalPointer = pointerAugment;
                    System.out.println("here2");
                    System.out.println(pointerAugment);
                } else {
                    keepSearching = false;
                }
                
                
//            if (highIndex-lowIndex < 2){
//                if ((searchArray[lowIndex] <= target) && (target <= searchArray[lowIndex+1])) {
//                    sharedVar.globalFound = true;
//                    sharedVar.globalPointer = pointerAugment+lowIndex+1;
//                    
//                } else if ((searchArray[lowIndex-1] <= target) && (target <= searchArray[lowIndex])) {
//                    sharedVar.globalFound = true;
//                    sharedVar.globalPointer = pointerAugment+lowIndex;
//                    
//                } else {
//                    keepSearching = false;
//                }
//                

            } else {
                System.out.println(pointer);
                System.out.println(searchArray[pointer-1]);
                System.out.println(searchArray[pointer]);
                if ((searchArray[pointer-1] < target) && (target <= searchArray[pointer] )){
                    sharedVar.globalFound = true;
                    sharedVar.globalPointer = pointer + pointerAugment;
                    System.out.println(pointer);
                    System.out.println(target);
                    for (double item : searchArray){
                        System.out.print(item);
                        System.out.print(" ");
                    }
                    System.out.println("");
                } else if (target <= searchArray[pointer-1]) {
                    highIndex = pointer-1;
                } else {
                    lowIndex = pointer+1;
                }
                
            pointer = (int) (lowIndex+Math.floor((highIndex-lowIndex)/2));
            
            }
        }
    }
}
