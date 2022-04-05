
public class SumChildren implements Runnable  {
    
    SearchTreeNodeVolatile[] nodes;    
    
    public SumChildren(SearchTreeNodeVolatile[] nodesParam){
        nodes = nodesParam;
    }
    
    public void run(){
        
        for (SearchTreeNodeVolatile node : nodes){
            double total = 0;

            for (SearchTreeNodeVolatile childNode : node.children){
                total = total+childNode.value;
            }

            node.value = total;
        }
    }
    
}
