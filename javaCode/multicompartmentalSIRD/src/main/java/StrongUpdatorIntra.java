/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Aaron Holdsworth
 */
public class StrongUpdatorIntra implements Runnable{
    
    SearchTreeNodeVolatile[] nodes;    
    IntraRule[] intraRuleList;
    Compartment[] compartmentList;
    Funct[] intraFuncts;
    int compartment;
    int index;
    double total;
    
    public StrongUpdatorIntra(SearchTreeNodeVolatile[] nodesParam, IntraRule[] intraRuleListParam,Compartment[] compartmentListParam, Funct[] intraFunctsParam,int compartmentParam, int startingIndex){
        nodes = nodesParam;
        intraRuleList = intraRuleListParam;
        compartmentList = compartmentListParam;
        intraFuncts = intraFunctsParam;
        compartment = compartmentParam;
        index = startingIndex;
        total=0;
    }
    
    public void run(){
        
        
        for (SearchTreeNodeVolatile node : nodes){
                        
            node.value = intraRuleList[index].calculatePropensity(intraFuncts[index].execute(compartmentList[compartment].intraParams[index],compartmentList[compartment]),compartmentList[compartment]);
                
            System.out.println(node.value);
            total = total+node.value;
            
            index++;
        }
    }
    
}
