
public class SumArray implements Runnable {
    
    double[] arrayToSum;
    double total;
    
    SumArray(double[] inputArray){
        arrayToSum = inputArray;
    }
    
    public void run(){
        
        total = 0;
        
        for (double item : arrayToSum){
            total = total+item;
        }
        
        
    }

}
