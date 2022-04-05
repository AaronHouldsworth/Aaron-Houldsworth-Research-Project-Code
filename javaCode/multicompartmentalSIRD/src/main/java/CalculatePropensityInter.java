
public class CalculatePropensityInter implements Runnable  {
    
    SearchTreeNodeVolatile[] nodes;
    int startIndex;
    int toCompartment;
    int fromCompartment;
    InterRule[] interRuleList;
    Funct[] interFuncts;
    Compartment[] compartmentList;
    
    
    public CalculatePropensityInter(SearchTreeNodeVolatile[] nodesParam ,int startIndexParam, int fromCompartmentParam, int toCompartmentParam, InterRule[] interRuleListParam, Funct[] interFunctsParam,Compartment[] compartmentListParam){
        nodes = nodesParam;
        startIndex = startIndexParam;
        fromCompartment = fromCompartmentParam;
        toCompartment = toCompartmentParam;
        interRuleList = interRuleListParam;
        interFuncts = interFunctsParam;
        compartmentList = compartmentListParam;
    }
    
    public void run(){
        for (int k = 0; k<nodes.length; k = k+1){
            nodes[k].value = interRuleList[k+startIndex].calculatePropensity(interFuncts[k+startIndex].execute(compartmentList[fromCompartment].interParams[k+startIndex][toCompartment],compartmentList[fromCompartment]),compartmentList[fromCompartment]);
            //System.out.println(nodes[k].value);
        }
        
    }
    
}
