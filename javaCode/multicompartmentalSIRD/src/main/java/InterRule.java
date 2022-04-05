
import java.lang.reflect.Array;


public class InterRule {
    
    int[] sourceComplex;
    int[] targetComplex;
    Maths M;
    
    
    public InterRule(int[] sourceComplex, int[] targetComplex, Maths M){
        this.sourceComplex = sourceComplex;
        this.targetComplex = targetComplex;
        this.M = M;
        
    }
    
    public void executeRule(Compartment fromCompartment,Compartment toCompartment){
        for (int i = 0; i < fromCompartment.noTypes; i = i + 1){
            Array.set(fromCompartment.typeList,i, fromCompartment.typeList[i] - this.sourceComplex[i]);
            Array.set(toCompartment.typeList,i, toCompartment.typeList[i] + this.sourceComplex[i]);
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
