
import java.lang.reflect.Array;


public class IntraRule {
    
    int[] sourceComplex;
    int[] targetComplex;
    Maths M;
    
    
    public IntraRule(int[] sourceComplex, int[] targetComplex, Maths M){
        this.sourceComplex = sourceComplex;
        this.targetComplex = targetComplex;
        this.M = M;
        
    }
    
    public void executeRule(Compartment compartment){
        for (int i = 0; i < compartment.noTypes; i = i + 1){
            Array.set(compartment.typeList,i, compartment.typeList[i] - this.sourceComplex[i] + this.targetComplex[i]);
        }
    }
    
    public double calculatePropensity(double kinetic, Compartment compartment){
        
        double total = kinetic;
        
        for (int i = 0; i < compartment.noTypes; i = i + 1){
            total = total*M.nCr(compartment.typeList[i], this.sourceComplex[i]);
        }
        
        return(total);
        
    }

}
