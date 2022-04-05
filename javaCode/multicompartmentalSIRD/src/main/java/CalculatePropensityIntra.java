
public class CalculatePropensityIntra implements Runnable  {
    
    SearchTreeNodeVolatile[] nodes;
    int startIndex;
    int compartment;
    IntraRule[] intraRuleList;
    Funct[] intraFuncts;
    Compartment[] compartmentList;
    
    
    public CalculatePropensityIntra(SearchTreeNodeVolatile[] nodesParam ,int startIndexParam, int compartmentParam, IntraRule[] intraRuleListParam, Funct[] intraFunctsParam,Compartment[] compartmentListParam){
        nodes = nodesParam;
        startIndex = startIndexParam;
        compartment = compartmentParam;
        intraRuleList = intraRuleListParam;
        intraFuncts = intraFunctsParam;
        compartmentList = compartmentListParam;
    }
    
    public void run(){
        for (int k = 0; k<nodes.length; k = k+1){
            nodes[k].value = intraRuleList[k+startIndex].calculatePropensity(intraFuncts[k+startIndex].execute(compartmentList[compartment].intraParams[k+startIndex],compartmentList[compartment]),compartmentList[compartment]);
            //System.out.println(nodes[k].value);
        }
        
    }
    
}
