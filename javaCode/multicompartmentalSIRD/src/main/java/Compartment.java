
public class Compartment {
    
    int[] typeList;
    int noTypes;
    int initPop;
    double[] intraParams;
    double[][] interParams;
    
    
    public Compartment(int[] typeListParam, double[] intraParamsParam, double[][] interParamsParam){

        this.typeList = typeListParam;
        this.intraParams = intraParamsParam;
        this.interParams = interParamsParam;
        
        this.noTypes = this.typeList.length;
        
        this.initPop = this.getPopInit();
        
    }
    
    public int getPopInit(){
        int total = 0;
        for (int type : this.typeList){
            total = total+type;
        }
        return(total);
    }
    
    public int getPopulation(){
        int total = 0;
        for (int type : this.typeList){
            total = total+type;
        }
            
        return(this.initPop);
    }
    
}
