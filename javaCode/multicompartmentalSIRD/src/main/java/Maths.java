public class Maths {
    
    public Maths(){}
    
    public static double factorial(double n){
        
        
        
        double retVal;
        
        if ((n==0) || (n==1)){
            retVal = 1;
        } else {
            retVal = n * factorial(n-1); 
        }
        
        return(retVal);
               
    }
    
    public int multFromTo(int start,int end){
        int value = 1;
        for(int i=start; i<=end; i++){
            value = value*i;
        }
        
        return(value);
    }
    public int multFromToDiv(int start,int end){
        int value = 1;
        int count = 1;
        for(int i=start; i<=end; i++){
            value = value*i/count;
            count = count+1;
        }
        
        return(value);
    }
    
    
    public int nCr(int n,int r){
       
        //System.out.println("ncr");
        //System.out.println(n);
        //System.out.println(r);
//        
//        int retVal;
//        
//        if (r>n){
//            retVal = 0;
//        } else if ((n==0) && (r==0)) {
//            retVal = 1;
//        } else if (r==0) {
//            retVal = 1;
//        } else {
//                        
//            retVal = (int) (factorial((double) n)/(factorial((double) r)*factorial((double) n-r)));
//            System.out.println(n);
//            System.out.println(factorial((double) n));
//            System.out.println(factorial((double) r));
//            System.out.println(factorial((double) n-r));
//            System.out.println("");
//        }
//
//        System.out.println(retVal);
//        return(retVal);




//        int retVal;
//        
//        if (r>n){
//            retVal = 0;
//        } else if ((n==0) && (r==0)) {
//            retVal = 1;
//        } else if (r==0) {
//            retVal = 1;
//        } else if (r>(n-r)){
//            retVal = multFromTo(r+1,n)/multFromTo(1,(n-r));
//        } else {
//            retVal = multFromTo((n-r)+1,n)/multFromTo(1,(r));
//        }
//        
//        return(retVal);
        
        int retVal;
        
        if (r>n){
            retVal = 0;
        } else if ((n==0) && (r==0)) {
            retVal = 1;
        } else if (r==0) {
            retVal = 1;
        } else if (r>(n-r)){
            retVal = multFromToDiv(r+1,n);
        } else {
            retVal = multFromToDiv((n-r)+1,n);
        }
        
        return(retVal);
    }
    
    

}
