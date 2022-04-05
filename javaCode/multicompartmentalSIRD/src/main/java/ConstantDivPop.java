
public class ConstantDivPop extends Funct {
    
    public ConstantDivPop(){}
    
    public double execute(double constant,Compartment compartment){
        double total = 0;
        
        for (int value : compartment.typeList ){
            
            total = total + value;
        }
        
        
        
        return(constant/total);
    }
    
}