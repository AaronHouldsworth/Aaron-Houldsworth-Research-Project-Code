import java.util.ArrayList;

public class SearchTreeNodeVolatile {
    
    volatile double value;
    volatile double sumValue;
    volatile ArrayList<SearchTreeNodeVolatile> children;
    
    public SearchTreeNodeVolatile(){
        this.children = new ArrayList<>();
        this.value = 0;
        this.sumValue = 0;
    }
    
    public SearchTreeNodeVolatile(float inputVal){
        this.children = new ArrayList<>();
        this.value = inputVal;
        this.sumValue = 0;
    }
    
    public void addChild(SearchTreeNodeVolatile child){
        this.children.add(child);
    }
    
    public double updateTreeValues(){
              
        
        
        if (this.children.size() > 0) {
            double total = 0;
            
            for (SearchTreeNodeVolatile child : this.children){
                total = total+child.updateTreeValues();
            }
            this.value = total;
        }
        
        
        return(this.value);
        
    }
    
    
    
    
    public double updateTreeSums(){
        
        if (this.children.size() > 0) {
            double total = 0;
            for (SearchTreeNodeVolatile child : this.children){
                total = total+child.updateTreeSums();
                child.sumValue = total;
            }
            this.value = total;
        }
        
        return(this.value);
    }
    
    public void updateSumFromOneChild(int index,double oldChildSum){
        this.value = this.value - oldChildSum + this.children.get(index).value;
    }

}

