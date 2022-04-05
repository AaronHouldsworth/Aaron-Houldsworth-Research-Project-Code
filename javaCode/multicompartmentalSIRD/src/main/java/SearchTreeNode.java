import java.util.ArrayList;

public class SearchTreeNode {
    
    double value;
    double sumValue;
    ArrayList<SearchTreeNode> children;
    
    public SearchTreeNode(){
        this.children = new ArrayList<>();
        this.value = 0;
        this.sumValue = 0;
    }
    
    public SearchTreeNode(float inputVal){
        this.children = new ArrayList<>();
        this.value = inputVal;
        this.sumValue = 0;
    }
    
    public void addChild(SearchTreeNode child){
        this.children.add(child);
    }
    
    public double updateTreeValues(){
              
        
        
        if (this.children.size() > 0) {
            double total = 0;
            
            for (SearchTreeNode child : this.children){
                total = total+child.updateTreeValues();
            }
            this.value = total;
        }
        
        
        return(this.value);
        
    }
    
    public double updateTreeSums(){
        
        if (this.children.size() > 0) {
            double total = 0;
            for (SearchTreeNode child : this.children){
                total = total+child.updateTreeSums();
                child.sumValue = total;
            }
            this.value = total;
        }
        
        return(this.value);
    }
    
    public void updateSumFromOneChild(int index,double oldChildSum){
        //System.out.println(this.sumValue - oldChildSum + this.children.get(index).value);
        this.value = this.value - oldChildSum + this.children.get(index).value;
    }

}

