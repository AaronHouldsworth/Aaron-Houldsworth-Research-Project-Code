/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Aaron Holdsworth
 */
public class StrongUpdatorInter implements Runnable{
    
    SearchTreeNodeVolatile[] nodes;    
    InterRule[] interRuleList;
    Compartment[] compartmentList;
    Funct[] interFuncts;
    int compartment;
    int index;
    double difference;
    
    public StrongUpdatorInter(SearchTreeNodeVolatile[] nodesParam, InterRule[] interRuleListParam,Compartment[] compartmentListParam, Funct[] interFunctsParam,int compartmentParam, int startingIndex){
        nodes = nodesParam;
        interRuleList = interRuleListParam;
        compartmentList = compartmentListParam;
        interFuncts = interFunctsParam;
        compartment = compartmentParam;
        index = startingIndex;
        difference = 0;
    }
    
    public void run(){
        
        
        
        for (SearchTreeNodeVolatile node : nodes){
            
            double total = 0;
            int ruleIndex = 0;

            for (SearchTreeNodeVolatile childNode : node.children){
                childNode.value = interRuleList[ruleIndex].calculatePropensity(interFuncts[ruleIndex].execute(compartmentList[compartment].interParams[ruleIndex][index],compartmentList[compartment]),compartmentList[compartment]);
                total = total+childNode.value;
                ruleIndex ++;
            }
            
            index++;

            difference = total-node.value;
            node.value = total;
            
        }
    }
    
}
