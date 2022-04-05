import java.io.FileWriter;
import java.util.ArrayList;
import java.lang.Math;
import java.util.Random;
import java.io.*;
import java.util.*;


public class Gillespie {
    
    Compartment[] compartmentList;
    IntraRule[] intraRuleList;
    InterRule[] interRuleList;
    float finTime;
    int maxIts;
    int noCompartments;
    int noTypes;
    int noIntraRules;
    int noInterRules;
    Funct[] intraFuncts;
    Funct[] interFuncts;
    SearchTreeNode root;
    volatile SearchTreeNodeVolatile rootV;
    
    
    
    public Gillespie(Compartment[] compartmentList,IntraRule[] intraRuleList,InterRule[] interRuleList,float finTime,int maxIts,Funct[] intraFuncts,Funct[] interFuncts){
        this.noCompartments = compartmentList.length;
        this.noTypes = compartmentList[0].noTypes;
        this.noIntraRules = intraRuleList.length;
        this.noInterRules = interRuleList.length;
        //System.out.println(noInterRules);
        //System.out.println(interFuncts.length);
        this.intraFuncts = intraFuncts;
        this.interFuncts = interFuncts;
        this.compartmentList = compartmentList;
        this.finTime = finTime;
        this.maxIts = maxIts;
        this.intraRuleList = intraRuleList;
        this.interRuleList = interRuleList;
        
        SearchTreeNode root = new SearchTreeNode();
        root.addChild(new SearchTreeNode());
        root.addChild(new SearchTreeNode());


        for (int i = 0; i<noCompartments; i = i+1){
            
            root.children.get(0).addChild(new SearchTreeNode());
            
            for (int j = 0; j<noIntraRules; j = j+1){
                
                root.children.get(0).children.get(i).addChild(new SearchTreeNode());     
                //intraRuleList.get(j).kineticConst = intraRuleList[j].kineticFunct(compartmentList[i].intraParams[j],compartmentList[i],compartmentList)
                //System.out.println(i);
                root.children.get(0).children.get(i).children.get(j).value = intraRuleList[j].calculatePropensity(intraFuncts[j].execute(compartmentList[i].intraParams[j],compartmentList[i]),compartmentList[i]);
                //System.out.println(root.children.get(0).children.get(i).children.get(j).value);
            }
        }
        
        for (int i = 0; i<noCompartments; i = i+1){
            
            root.children.get(1).addChild(new SearchTreeNode());

            for (int j = 0; j<(noCompartments-1); j = j+1){
                root.children.get(1).children.get(i).addChild(new SearchTreeNode());

                for (int k = 0; k<noInterRules; k = k+1){
                    root.children.get(1).children.get(i).children.get(j).addChild(new SearchTreeNode());
                    //interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[k].interParams[i][k][j],compartmentList[j])
                    //interRuleList[k].kineticConst = interRuleList[k].kineticFunct(compartmentList[i].interParams[k][i][j],compartmentList[i],compartmentList)
                    //System.out.println("Rule");
                    //System.out.println(i);
                    
                    //System.out.println(k);
                    root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[k].calculatePropensity(interFuncts[k].execute(compartmentList[i].interParams[k][j],compartmentList[i]),compartmentList[i]);
                    }
            }
        }
        
                
        //root.updateTreeValues(0);
        this.root = root;
        //this.printTree4();
        
        this.root.updateTreeSums();
        //this.printTree4();
        
        
        SearchTreeNodeVolatile rootV = new SearchTreeNodeVolatile();
        rootV.addChild(new SearchTreeNodeVolatile());
        rootV.addChild(new SearchTreeNodeVolatile());


        for (int i = 0; i<noCompartments; i = i+1){
            
            rootV.children.get(0).addChild(new SearchTreeNodeVolatile());
            
            for (int j = 0; j<noIntraRules; j = j+1){
                
                rootV.children.get(0).children.get(i).addChild(new SearchTreeNodeVolatile());     
                //intraRuleList.get(j).kineticConst = intraRuleList[j].kineticFunct(compartmentList[i].intraParams[j],compartmentList[i],compartmentList)
                rootV.children.get(0).children.get(i).children.get(j).value = intraRuleList[j].calculatePropensity(intraFuncts[j].execute(compartmentList[i].intraParams[j],compartmentList[i]),compartmentList[i]);
                
            }
        }
        
        for (int i = 0; i<noCompartments; i = i+1){
            
            rootV.children.get(1).addChild(new SearchTreeNodeVolatile());

            for (int j = 0; j<(noCompartments-1); j = j+1){
                rootV.children.get(1).children.get(i).addChild(new SearchTreeNodeVolatile());

                for (int k = 0; k<(noInterRules); k = k+1){
                    rootV.children.get(1).children.get(i).children.get(j).addChild(new SearchTreeNodeVolatile());
                    //interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[k].interParams[i][k][j],compartmentList[j])
                    //interRuleList[k].kineticConst = interRuleList[k].kineticFunct(compartmentList[i].interParams[k][i][j],compartmentList[i],compartmentList)
                    
                    rootV.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[k].calculatePropensity(interFuncts[k].execute(compartmentList[i].interParams[k][j],compartmentList[i]),compartmentList[i]);
                    }
            }
        }
        
                
        //root.updateTreeValues(0);
        this.rootV = rootV;
        //this.printVTree4();
        
        this.rootV.updateTreeSums();
        //this.printVTree4();
        
            
    }
    
    public ArrayList runLinear(){
        
        Random rand = new Random(1);
        
        double time = 0;
        double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        for (Compartment thisCompartment : compartmentList){
            for (int i = 0; i<noTypes; i = i+1){
                data[0][i][count] = thisCompartment.typeList[i];
            }
            count = count+1;
        }
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.root.updateTreeValues();
        
        int iteration = 0;
        
        
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = root.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;

            if (r2*R0>root.children.get(0).value){

                ruleType = 1;

                double target = r2*R0 - root.children.get(0).value;

                ArrayList searchData = this.linearSearch(target, root.children.get(1));

                fromCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(1).children.get(fromCompartment));

                toCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(1).children.get(fromCompartment).children.get(toCompartment));
                
                rule = (int) searchData.get(0);

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;

                ArrayList searchData = this.linearSearch(target, root.children.get(0));
                
                compartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(0).children.get(compartment));
                
                rule = (int) searchData.get(0);
                
            }
            
            if (ruleType == 0) {
                
                intraRuleList[rule].executeRule(compartmentList[compartment]);
                
                for (int i = 0; i<noCompartments; i=i+1){
                    for (int j = 0; j<noCompartments-1; j=j+1){
                        for (int k = 0; k<noInterRules;k=k+1){
                            if (j>=i){
                                int modifier = 1;
                            } else {
                                int modifier = 0 ;
                            }
                            
                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[k].calculatePropensity(interFuncts[k].execute(compartmentList[i].interParams[k][j],compartmentList[i]),compartmentList[i]);
                        }
                    }
                }

                for (int i=0; i<noCompartments; i=i+1){
                    for (int j=0; j<noIntraRules; j=j+1){ 
                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[j].calculatePropensity(intraFuncts[j].execute(compartmentList[i].intraParams[j],compartmentList[i]),compartmentList[i]);
                    }
                }
                
                root.updateTreeValues();
            
            } else {
                if (fromCompartment <= toCompartment){
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
                } else {
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
                }
                
                for (int i = 0; i< noCompartments; i = i+1){
                    for (int j = 0; j < noCompartments-1; j = j+1){
                        for (int k = 0; k < noInterRules; k = k+1){
                            if (j>=i){
                                int modifier = 1;
                            } else {
                                int modifier = 0;
                            }
                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[k].calculatePropensity(interFuncts[k].execute(compartmentList[i].interParams[k][j],compartmentList[i]),compartmentList[i]);
                        }
                    }
                }
                
                for (int i=0; i<noCompartments; i=i+1){
                    for (int j=0; j<noIntraRules; j=j+1){    
                        
                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[j].calculatePropensity(intraFuncts[j].execute(compartmentList[i].intraParams[j],compartmentList[i]),compartmentList[i]);
                    }
                }
                
                root.updateTreeValues();
                                
            }
            
            //System.out.println(iteration);
            count = 0;
            for (Compartment thisCompartment : compartmentList){
                for (int i = 0; i<noTypes; i = i+1){
                    data[iteration][i][count] = thisCompartment.typeList[i];
                    
                    //System.out.print(thisCompartment.typeList[i]);
                    //System.out.print(" ");
                }
                //System.out.println();
                count = count+1;
                
            }
            
            timeData[iteration]=time;
            
            //System.out.println(iteration);
            
//            if (ruleType==0){
//                System.out.println(compartment);
//                System.out.println(rule);
//            } else {
//                System.out.println(fromCompartment);
//                System.out.println(toCompartment);
//                System.out.println(rule);
//            }
//            this.printTree4();
//            System.out.println("");
            //System.out.println("");
            //System.out.print("compartment ");
            //System.out.print(compartment);
            //System.out.print("   rule ");
            //System.out.println(rule);
            //printTree4();
            
            
        }
        
        ArrayList retList = new ArrayList<>(); 
        
        retList.add(data);
        retList.add(timeData);
        retList.add(iteration);
        
        
        
        return(retList);
        
        
    }


    //public ArrayList runLinearStrong() throws IOException{
    public int[] runLinearStrong() throws IOException{
        
//        FileWriter[] csvWriters = new FileWriter[noCompartments];
//        for (int i=0; i<noCompartments; i = i+1){
//            String titleText = "compData"+i+".txt";
//            csvWriters[i] = new FileWriter(titleText);
//        }
        
        double printTime = 1;
        
        Random rand = new Random();
        
        double time = 0;
        //double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        //double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        //for (Compartment thisCompartment : compartmentList){
        //    for (int i = 0; i<noTypes; i = i+1){
        //        data[0][i][count] = thisCompartment.typeList[i];
        //    }
        //    count = count+1;
        //}
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.root.updateTreeValues();
        
        int iteration = 0;
        
        int[] infectionFlag = new int[]{0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,1};
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = root.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;

            if (r2*R0>root.children.get(0).value){

                ruleType = 1;

                
                
                double target = r2*R0 - root.children.get(0).value;
                
                

                ArrayList searchData = this.linearSearch(target, root.children.get(1));

                fromCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(1).children.get(fromCompartment));

                toCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(1).children.get(fromCompartment).children.get(toCompartment));
                
                rule = (int) searchData.get(0);

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;

                ArrayList searchData = this.linearSearch(target, root.children.get(0));
                
                compartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearch(target, root.children.get(0).children.get(compartment));
                
                rule = (int) searchData.get(0);
                
                
            }
            
            
            if (ruleType==0){
            
                intraRuleList[rule].executeRule(compartmentList[compartment]);

                IntraRule selectedRule = intraRuleList[rule];

                double oldSum2 = root.children.get(0).children.get(compartment).value;
                //System.out.print("oldSum2: ");
                //System.out.println(oldSum2);
                double oldSum3 = root.children.get(0).value;
                //System.out.print("oldSum3: ");
                //System.out.println(oldSum3);

                for (int i = 0; i<intraRuleList.length; i++){
                    double oldSum1 = root.children.get(0).children.get(compartment).children.get(i).value;
                    //System.out.print("oldSum1: ");
                    //System.out.println(oldSum1);
                    
                    
                    root.children.get(0).children.get(compartment).children.get(i).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[compartment].intraParams[i],compartmentList[compartment]),compartmentList[compartment]);
                    
                    //root.children.get(0).children.get(compartment).children.get(i).value = intraRuleList[i].calculatePropensity(compartmentList[compartment].intraParams[i],compartmentList[compartment]);
                       
                    //System.out.print("before update: ");
                    //System.out.println(root.children.get(0).children.get(compartment).children.get(i));
                    root.children.get(0).children.get(compartment).updateSumFromOneChild(i, oldSum1);
                    //System.out.print("updated node: ");
                    //System.out.println(root.children.get(0).children.get(compartment).children.get(i));

                }
                root.children.get(0).updateSumFromOneChild(compartment,oldSum2);
                root.updateSumFromOneChild(0,oldSum3);


                oldSum3 = root.children.get(1).children.get(compartment).value;
                double oldSum4 = root.children.get(1).value;

                for (int i=0; i<interRuleList.length; i++){

                    for (int k=0; k<noCompartments-1; k++){

                        double oldSum1 = root.children.get(1).children.get(compartment).children.get(k).children.get(i).value;
                        oldSum2 = root.children.get(1).children.get(compartment).children.get(k).value;

                        root.children.get(1).children.get(compartment).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[compartment].interParams[i][k],compartmentList[compartment]),compartmentList[compartment]);
                        //root.children.get(1).children.get(compartment).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(compartmentList[compartment].interParams[i][k],compartmentList[compartment]);

                        root.children.get(1).children.get(compartment).children.get(k).updateSumFromOneChild(i,oldSum1);
                        root.children.get(1).children.get(compartment).updateSumFromOneChild(k,oldSum2);
                    }    
                }
                root.children.get(1).updateSumFromOneChild(compartment,oldSum3);
                root.updateSumFromOneChild(1,oldSum4);

            
            } else {
                
                int modifier;

                if (fromCompartment <= toCompartment){
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
                    modifier = 1;
                } else {
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
                    modifier = 0;
                }

                InterRule selectedRule = interRuleList[rule];


                double oldSum2 = root.children.get(0).children.get(fromCompartment).value;
                double oldSum3 = root.children.get(0).value;
                for (int i=0; i<intraRuleList.length; i++){
                  
                    double oldSum1 = root.children.get(0).children.get(fromCompartment).children.get(i).value;
                    
                    root.children.get(0).children.get(fromCompartment).children.get(i).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[fromCompartment].intraParams[i],compartmentList[fromCompartment]),compartmentList[fromCompartment]);
                    //System.out.println(fromCompartment);
                    //System.out.println(root.children.get(0).children.get(fromCompartment).children.get(i).value);
                    //root.children.get(0).children.get(fromCompartment).children.get(i).value = intraRuleList[i].calculatePropensity(compartmentList[fromCompartment].intraParams[i],compartmentList[fromCompartment]);

                    //root.children.get(0).children.get(i).children.get(j).value = intraRuleList[j].calculatePropensity(intraFuncts[j].execute(compartmentList[i].intraParams[j],compartmentList[i]),compartmentList[i]);
                    
                    
                    root.children.get(0).children.get(fromCompartment).updateSumFromOneChild(i,oldSum1);
                }
                root.children.get(0).updateSumFromOneChild(fromCompartment,oldSum2);
                root.updateSumFromOneChild(0,oldSum3);
                

                oldSum2 = root.children.get(0).children.get(toCompartment+modifier).value;
                oldSum3 = root.children.get(0).value;

                for (int i=0;i<intraRuleList.length;i++){            

                    double oldSum1 = root.children.get(0).children.get(toCompartment+modifier).children.get(i).value;

                    root.children.get(0).children.get(toCompartment+modifier).children.get(i).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[toCompartment+modifier].intraParams[i],compartmentList[toCompartment+modifier]),compartmentList[toCompartment+modifier]);
                    //root.children.get(0).children.get(toCompartment).children.get(i).value = intraRuleList[i].calculatePropensity(compartmentList[toCompartment].intraParams[i],compartmentList[toCompartment]);
                    
                    //System.out.println(toCompartment+modifier);
                    //System.out.println(root.children.get(0).children.get(toCompartment+modifier).children.get(i).value);
                    root.children.get(0).children.get(toCompartment+modifier).updateSumFromOneChild(i,oldSum1);
                }
                root.children.get(0).updateSumFromOneChild(toCompartment+modifier,oldSum2);
                root.updateSumFromOneChild(0,oldSum3);


                oldSum3 = root.children.get(1).children.get(fromCompartment).value;
                double oldSum4 = root.children.get(1).value;

                for (int k=0; k<noCompartments-1; k++){
                    
                    oldSum2 = root.children.get(1).children.get(fromCompartment).children.get(k).value;
                    
                    for (int i=0; i<interRuleList.length; i++){

                        double oldSum1 = root.children.get(1).children.get(fromCompartment).children.get(k).children.get(i).value;
                        
                        root.children.get(1).children.get(fromCompartment).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[fromCompartment].interParams[i][k],compartmentList[fromCompartment]),compartmentList[fromCompartment]);
                        //root.children.get(1).children.get(fromCompartment).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(compartmentList[fromCompartment].interParams[i][k],compartmentList[fromCompartment]);

                        root.children.get(1).children.get(fromCompartment).children.get(k).updateSumFromOneChild(i,oldSum1);
                    }
                    root.children.get(1).children.get(fromCompartment).updateSumFromOneChild(k,oldSum2);
                }
                root.children.get(1).updateSumFromOneChild(fromCompartment,oldSum3);
                root.updateSumFromOneChild(1,oldSum4);


                oldSum3 = root.children.get(1).children.get(toCompartment+modifier).value;
                oldSum4 = root.children.get(1).value;
                for (int k=0; k<noCompartments-1; k++){
                    
                    oldSum2 = root.children.get(1).children.get(toCompartment+modifier).children.get(k).value;
                    for (int i=0; i<interRuleList.length; i++){

                        double oldSum1 = root.children.get(1).children.get(toCompartment+modifier).children.get(k).children.get(i).value;

                        root.children.get(1).children.get(toCompartment+modifier).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[toCompartment+modifier].interParams[i][k],compartmentList[toCompartment+modifier]),compartmentList[toCompartment+modifier]);
                        //root.children.get(1).children.get(toCompartment).children.get(k).children.get(i).value = interRuleList[i].calculatePropensity(compartmentList[toCompartment].interParams[i][k],compartmentList[toCompartment]);

                        root.children.get(1).children.get(toCompartment+modifier).children.get(k).updateSumFromOneChild(i,oldSum1);
                    }
                    root.children.get(1).children.get(toCompartment+modifier).updateSumFromOneChild(k,oldSum2);
                }
                root.children.get(1).updateSumFromOneChild(toCompartment+modifier,oldSum3);
                root.updateSumFromOneChild(1,oldSum4);
            }
            //System.out.println(iteration);
//            count = 0;
//            for (Compartment thisCompartment : compartmentList){
//                for (int i = 0; i<noTypes; i = i+1){
//                    data[iteration][i][count] = thisCompartment.typeList[i];
//                    //System.out.print(thisCompartment.typeList[i]);
//                    //System.out.print(" ");
//                }
//                //System.out.println();
//                count = count+1;
//                
//            }
            
//            if (ruleType==0){
//                System.out.println(compartment);
//                System.out.println(rule);
//            } else {
//                System.out.println(fromCompartment);
//                System.out.println(toCompartment);
//                System.out.println(rule);
//            }
            //this.printTree4();
            //System.out.println("");
            
//            printTime = printTime+timeIncrement;
//            if (printTime>1){
//                System.out.println(time);
//                printTime = printTime-1;
//                
////                for (int j=0; j<noCompartments; j = j+1){
////                    
////                    csvWriters[j].append(Integer.toString(compartmentList[j].typeList[0]));
////                    csvWriters[j].append(",");
////                    csvWriters[j].append(Integer.toString(compartmentList[j].typeList[1]));
////                    csvWriters[j].append(",");
////                    csvWriters[j].append(Integer.toString(compartmentList[j].typeList[2]));
////                    csvWriters[j].append(",");
////                    csvWriters[j].append(Integer.toString(compartmentList[j].typeList[3]));
////                    csvWriters[j].append("\n");
////                          
////                }
////                
//                //Code for grid output
//                for (int a=0; a<10; a++){
//                    for (int b=0; b<10; b++){
//                        System.out.print("   (");
//                        System.out.print(compartmentList[a*10+b].typeList[0]);
//                        System.out.print(",");
//                        System.out.print(compartmentList[a*10+b].typeList[1]);
//                        System.out.print(",");
//                        System.out.print(compartmentList[a*10+b].typeList[2]);
//                        System.out.print(",");
//                        System.out.print(compartmentList[a*10+b].typeList[3]);
//                        System.out.print(")   ");
//                    }
//                    System.out.println("");
//                }
//                System.out.println("");
//                
////
////                //   code for line output
////                for (int a=0; a<10; a++){
////                    System.out.print("   (");
////                    System.out.print(compartmentList[a].typeList[0]);
////                    System.out.print(",");
////                    System.out.print(compartmentList[a].typeList[1]);
////                    System.out.print(",");
////                    System.out.print(compartmentList[a].typeList[2]);
////                    System.out.print(",");
////                    System.out.print(compartmentList[a].typeList[3]);
////                    System.out.print(")   ");
////                }
////                System.out.println("");
//////            
//            }
            
            //timeData[iteration] = time;
            
            for (int a=0; a<100; a++){
                if ( (infectionFlag[a]==0) && compartmentList[a].typeList[1]>0){
                    infectionFlag[a] = 1;
                    //System.out.print("\n\n\n\n\n\n infection \n\n\n\n\n\n\n");
                }
            }
            
            int total = 0;
            for (int a=0;a<100;a++){
                total = total+compartmentList[a].typeList[1];
            }
            
            if (total==0){
                break;
            }
            
            
//            
            
        }
        
        
        
//        ArrayList retList = new ArrayList<>(); 
//        
//        retList.add(data);
//        retList.add(timeData);
//        retList.add(iteration);
        
        
        
        //System.out.println(compartmentList[0].typeList[1]);
        //System.out.println(compartmentList[0].typeList[0]);
//        for (int j=0; j<noCompartments; j = j+1){
//            
//            csvWriters[j].flush();
//            csvWriters[j].close();    
//
//        }
        
        
        //return(retList);
        int total = 0;
        for (int a=0;a<100;a++){
            total = total+compartmentList[a].typeList[1];
        }
        
        infectionFlag[100] = total;
        
        return(infectionFlag);
        
        
    }
    
    
    
    
    public ArrayList runBinary(){
        
        Random rand = new Random(0);
        
        double time = 0;
        double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        for (Compartment thisCompartment : compartmentList){
            for (int i = 0; i<noTypes; i = i+1){
                data[0][i][count] = thisCompartment.typeList[i];
            }
            count = count+1;
        }
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.root.updateTreeSums();
        
        int iteration = 0;
        
        
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = root.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;

            if (r2*R0>root.children.get(0).value){

                ruleType = 1;

                double target = r2*R0 - root.children.get(0).value;

                rule = binarySearch(target,root.children.get(1));

                if (rule>0){
                    target = target - (double) root.children.get(1).children.get(rule-1).sumValue;
                }
                
                fromCompartment = binarySearch(target,root.children.get(1).children.get(rule));

                if (fromCompartment>0){
                    target = target - (double) root.children.get(1).children.get(rule).children.get(fromCompartment-1).sumValue;
                }
                
                toCompartment = binarySearch(target,root.children.get(1).children.get(rule).children.get(fromCompartment));

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;

                rule = binarySearch(target,root.children.get(0));

                if (rule>0){
                    target = target - (double) root.children.get(0).children.get(rule-1).sumValue;
                }
                
                compartment = binarySearch(target,root.children.get(0).children.get(rule));
                
            }
            
            if (ruleType == 0) {
                
                intraRuleList[rule].executeRule(compartmentList[compartment]);
                
                for (int i = 0; i<noInterRules; i=i+1){
                    for (int j = 0; j<noCompartments; j=j+1){
                        for (int k = 0; k<noCompartments-1;k=k+1){
                            if (k>=j){
                                int modifier = 1;
                            } else {
                                int modifier = 0 ;
                            }
                            
                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[j].interParams[i][k],compartmentList[j]),compartmentList[j]);
                        }
                    }
                }

                for (int i=0; i<noIntraRules; i=i+1){
                    for (int j=0; j<noCompartments; j=j+1){ 
                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[j].intraParams[i],compartmentList[j]),compartmentList[j]);
                    }
                }
                
                root.updateTreeSums();
            
            } else {
                if (fromCompartment <= toCompartment){
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
                } else {
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
                }
                
                for (int i = 0; i< noInterRules; i = i+1){
                    for (int j = 0; j < noCompartments; j = j+1){
                        for (int k = 0; k < noCompartments-1; k = k+1){
                            if (j>=i){
                                int modifier = 1;
                            } else {
                                int modifier = 0;
                            }
                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[j].interParams[i][k],compartmentList[j]),compartmentList[j]);
                        }
                    }
                }
                
                for (int i=0; i<noIntraRules; i=i+1){
                    for (int j=0; j<noCompartments; j=j+1){    
                        
                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[j].intraParams[i],compartmentList[j]),compartmentList[j]);
                    }
                }
                
                root.updateTreeSums();
                                
            }
            
            count = 0;
            for (Compartment thisCompartment : compartmentList){
                for (int i = 0; i<noTypes; i = i+1){
                    data[0][i][count] = thisCompartment.typeList[i];
                    
                }
                count = count+1;
                
            }
            
            //System.out.println("");
            //System.out.print("compartment ");
            //System.out.print(compartment);
            //System.out.print("   rule ");
            //System.out.println(rule);
            //printTree4();
            
        }
        
        ArrayList retList = new ArrayList<>(); 
        
        retList.add(data);
        retList.add(timeData);
        retList.add(iteration);
        
        
        
        return(retList);
        
        
    }

    
    public ArrayList runLinearThreading(int noThreads) throws InterruptedException{
        
        Random rand = new Random(1);
        
        double time = 0;
        double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        for (Compartment thisCompartment : compartmentList){
            for (int i = 0; i<noTypes; i = i+1){
                data[0][i][count] = thisCompartment.typeList[i];
            }
            count = count+1;
        }
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.rootV.updateTreeValues();
        
        int iteration = 0;
        
        
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = rootV.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;

            if (r2*R0>rootV.children.get(0).value){

                ruleType = 1;

                double target = r2*R0 - rootV.children.get(0).value;

                ArrayList searchData = this.linearSearchThreading(rootV.children.get(1),target,noThreads);

                fromCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(1).children.get(fromCompartment),target,noThreads);

                toCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(1).children.get(fromCompartment).children.get(toCompartment),target,noThreads);
                
                rule = (int) searchData.get(0);

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;

                ArrayList searchData = this.linearSearchThreading(rootV.children.get(0),target,noThreads);
                
                compartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(0).children.get(compartment),target,noThreads);
                
                rule = (int) searchData.get(0);
                
            }


            updatePropensitiesThreading(noThreads,rootV,ruleType,rule,compartment,fromCompartment,toCompartment);
                       
            count = 0;
            for (Compartment thisCompartment : compartmentList){
                for (int i = 0; i<noTypes; i = i+1){
                    data[iteration][i][count] = thisCompartment.typeList[i];
                    
                    System.out.print(thisCompartment.typeList[i]);
                    System.out.print(" ");
                }
                System.out.println();
                count = count+1;
                
            }
            
            timeData[iteration]=time;
            
            System.out.println("");
            printVTree4();
            System.out.println("");
            
        }
        
        ArrayList retList = new ArrayList<>(); 
        
        retList.add(data);
        retList.add(timeData);
        retList.add(iteration);
        
        
        
        return(retList);
        
        
    }
    
        
    public ArrayList runLinearStrongThreading(int noThreads) throws InterruptedException{
        
        Random rand = new Random(1);
        
        double time = 0;
        double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        for (Compartment thisCompartment : compartmentList){
            for (int i = 0; i<noTypes; i = i+1){
                data[0][i][count] = thisCompartment.typeList[i];
            }
            count = count+1;
        }
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.rootV.updateTreeValues();
        
        int iteration = 0;
        
        
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = rootV.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;

            if (r2*R0>rootV.children.get(0).value){

                ruleType = 1;

                double target = r2*R0 - rootV.children.get(0).value;

                ArrayList searchData = this.linearSearchThreading(rootV.children.get(1),target,noThreads);

                fromCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(1).children.get(fromCompartment),target,noThreads);

                toCompartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(1).children.get(fromCompartment).children.get(toCompartment),target,noThreads);
                
                rule = (int) searchData.get(0);

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;

                ArrayList searchData = this.linearSearchThreading(rootV.children.get(0),target,noThreads);
                
                compartment = (int) searchData.get(0);

                target = target - (double) searchData.get(1);
                
                searchData = this.linearSearchThreading(rootV.children.get(0).children.get(compartment),target,noThreads);
                
                rule = (int) searchData.get(0);
                
            }

//---------------------------------------------------
            if (ruleType==0){
            
                intraRuleList[rule].executeRule(compartmentList[compartment]);

                this.updateNodesThreadingIntra(noThreads,compartment);
                
                this.updateNodesThreadingInter(noThreads,compartment);
                
            
            } else {
                
                int modifier;

                if (fromCompartment <= toCompartment){
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
                    modifier = 1;
                } else {
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
                    modifier = 0;
                }

                this.updateNodesThreadingIntra(noThreads,fromCompartment);
                
                this.updateNodesThreadingIntra(noThreads,toCompartment+modifier);

                this.updateNodesThreadingInter(noThreads,fromCompartment);
                
                this.updateNodesThreadingInter(noThreads,toCompartment+modifier);
            }
//---------------------------------------------------
            //updatePropensitiesThreading(noThreads,rootV,ruleType,rule,compartment,fromCompartment,toCompartment);
                       
            count = 0;
            for (Compartment thisCompartment : compartmentList){
                for (int i = 0; i<noTypes; i = i+1){
                    data[iteration][i][count] = thisCompartment.typeList[i];
                    
                    System.out.print(thisCompartment.typeList[i]);
                    System.out.print(" ");
                }
                System.out.println();
                count = count+1;
                
            }
            
            timeData[iteration]=time;
            
//            System.out.println("");
//            System.out.print("compartment ");
//            System.out.print(compartment);
//            System.out.print("   rule ");
//            System.out.println(rule);
            System.out.println("");
            printVTree4();
            System.out.println("");
            
        }
        
        ArrayList retList = new ArrayList<>(); 
        
        retList.add(data);
        retList.add(timeData);
        retList.add(iteration);
        
        
        
        return(retList);
        
        
    }    

    public ArrayList runBinaryThreading(int noThreads) throws InterruptedException{
        
        System.out.println("\n\n");
        
        Random rand = new Random(0);
        
        double time = 0;
        double[][][] data = new double[maxIts+1][noTypes][noCompartments];
        double[] timeData = new double[maxIts+1];
        
        int count = 0;
        
        for (Compartment thisCompartment : compartmentList){
            for (int i = 0; i<noTypes; i = i+1){
                data[0][i][count] = thisCompartment.typeList[i];
            }
            count = count+1;
        }
        
        int compartment = 0;
        int fromCompartment = 0;
        int toCompartment = 0;
        int rule = 0;
        
        this.rootV.updateTreeValues();
        
        int iteration = 0;
        
        
        
        while ((time<finTime) && (iteration<maxIts)){
            
            
            
            iteration = iteration+1;
       
            double R0 = rootV.value;
            double r1 = rand.nextDouble();
            
            double timeIncrement = -Math.log(r1)/R0;
        
            time = time+timeIncrement;

            double r2 = rand.nextDouble();
        
            int ruleType;
            
//            System.out.print("target: ");
//            System.out.println(r2*R0);
//            printVTree4();
//            printVTree4Bin();

            if (r2*R0>rootV.children.get(0).value){

                ruleType = 1;

                double target = r2*R0 - rootV.children.get(0).value;
//                System.out.print("Rule type: ");
//                System.out.print(ruleType);
//                System.out.print("    Target: ");
//                System.out.println(target);

                
                rule = (int) this.binarySearchThreading(rootV.children.get(1),target,noThreads);

                if (rule>0){
                    target = target - rootV.children.get(1).children.get(rule-1).sumValue;
                }
//                System.out.print("Rule ");
//                System.out.print(rule);
//                System.out.print("    Target: ");
//                System.out.println(target);
                
                fromCompartment = (int) this.binarySearchThreading(rootV.children.get(1).children.get(rule),target,noThreads);

                if (fromCompartment>0){
                    target = target - rootV.children.get(1).children.get(rule).children.get(fromCompartment).sumValue;
                }
//                System.out.print("From compartment: ");
//                System.out.print(fromCompartment);
//                System.out.print("    Target: ");
//                System.out.println(target);
                
                toCompartment = (int) this.binarySearchThreading(rootV.children.get(1).children.get(rule).children.get(fromCompartment),target,noThreads);
                
//                System.out.print("To compartment: ");
//                System.out.println(toCompartment);

            } else {
                
                ruleType = 0;
                
                double target = r2*R0;
                
//                System.out.print("Rule type: ");
//                System.out.print(ruleType);
//                System.out.print("    Target: ");
//                System.out.println(target);

                rule = (int) this.binarySearchThreading(rootV.children.get(0),target,noThreads);

                if (rule>0){
                    target = target - rootV.children.get(0).children.get(rule-1).sumValue;
                }
//                System.out.print("Rule ");
//                System.out.print(rule);
//                System.out.print("    Target: ");
//                System.out.println(target);
                
                compartment = (int) this.binarySearchThreading(rootV.children.get(0).children.get(rule),target,noThreads);

                if (compartment>0){
                    target = target - rootV.children.get(0).children.get(rule).children.get(compartment).sumValue;
                }
                
//                System.out.print("Compartment: ");
//                System.out.println(compartment);
                
                
            }
//            
//            if (ruleType == 0) {
//                
//                intraRuleList[rule].executeRule(compartmentList[compartment]);
//                
//                for (int i = 0; i<noInterRules; i=i+1){
//                    for (int j = 0; j<noCompartments; j=j+1){
//                        for (int k = 0; k<noCompartments-1;k=k+1){
//                            if (k>=j){
//                                int modifier = 1;
//                            } else {
//                                int modifier = 0 ;
//                            }
//                            
//                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[j].interParams[i][k],compartmentList[j]),compartmentList[j]);
//                        }
//                    }
//                }
//
//                for (int i=0; i<noIntraRules; i=i+1){
//                    for (int j=0; j<noCompartments; j=j+1){ 
//                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[j].intraParams[i],compartmentList[j]),compartmentList[j]);
//                    }
//                }
//                
//                root.updateTreeSums();
//            
//            } else {
//                if (fromCompartment <= toCompartment){
//                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
//                } else {
//                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
//                }
//                
//                for (int i = 0; i< noInterRules; i = i+1){
//                    for (int j = 0; j < noCompartments; j = j+1){
//                        for (int k = 0; k < noCompartments-1; k = k+1){
//                            if (j>=i){
//                                int modifier = 1;
//                            } else {
//                                int modifier = 0;
//                            }
//                            root.children.get(1).children.get(i).children.get(j).children.get(k).value = interRuleList[i].calculatePropensity(interFuncts[i].execute(compartmentList[j].interParams[i][k],compartmentList[j]),compartmentList[j]);
//                        }
//                    }
//                }
//                
//                for (int i=0; i<noIntraRules; i=i+1){
//                    for (int j=0; j<noCompartments; j=j+1){    
//                        
//                        root.children.get(0).children.get(i).children.get(j).value = intraRuleList[i].calculatePropensity(intraFuncts[i].execute(compartmentList[j].intraParams[i],compartmentList[j]),compartmentList[j]);
//                    }
//                }
//                
//                root.updateTreeSums();
//                                
//            }

            updatePropensitiesThreading(noThreads,rootV,ruleType,rule,compartment,fromCompartment,toCompartment);
            rootV.updateTreeSums();
                       
            count = 0;
            for (Compartment thisCompartment : compartmentList){
                for (int i = 0; i<noTypes; i = i+1){
                    data[0][i][count] = thisCompartment.typeList[i];
                    
                }
                count = count+1;
                
            }
            
//            System.out.println("");
//            System.out.print("compartment ");
//            System.out.print(compartment);
//            System.out.print("   rule ");
//            System.out.println(rule);
//            printVTree4();
            
            
        }
        
        ArrayList retList = new ArrayList<>(); 
        
        retList.add(data);
        retList.add(timeData);
        retList.add(iteration);
        
        
        
        return(retList);
        
        
    }
    
    
    
    
    private ArrayList linearSearch(double target,SearchTreeNode node){
        
//        System.out.print("target:");
//        System.out.println(target);
        
        double currentTotal = 0;
        int currentIndex = 0;
        boolean targetFound = false;
        
        ArrayList retList = new ArrayList<>(); 
        
        while (!(targetFound)){
            
            if ((target<1E-10) && (node.children.get(currentIndex).value<1E-10)){
                targetFound = true;
                break;
            }
            
            //System.out.println("here");
            //System.out.println(currentTotal);
            //System.out.println(target);
            //System.out.println(currentTotal+node.children.get(currentIndex).value);
            if ((currentTotal<=target) && (target<=currentTotal+node.children.get(currentIndex).value)){
                targetFound = true;
                
            }else{
                currentTotal = currentTotal+node.children.get(currentIndex).value;
                currentIndex = currentIndex+1;
            }
                        
        }
//        System.out.println(currentIndex);
//        System.out.println(currentTotal);
        retList.add(currentIndex);
        retList.add(currentTotal);
        
        return(retList);
    }
    
    private void printTree4(){
        
        
        System.out.println(root.value);
        System.out.print(root.children.get(0).value);
        System.out.print("|");
        System.out.println(this.root.children.get(1).value);
        
        System.out.print("|");
        for (SearchTreeNode child : root.children){
            for (SearchTreeNode grandChild : child.children){
                System.out.print(grandChild.value);
                System.out.print(" ");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNode child : root.children){
            for (SearchTreeNode grandChild : child.children){
                for (SearchTreeNode greatGrandChild: grandChild.children){
                    System.out.print(greatGrandChild.value);
                    System.out.print(" ");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNode child : root.children){
            for (SearchTreeNode grandChild : child.children){
                for (SearchTreeNode greatGrandChild: grandChild.children){
                    for (SearchTreeNode greatGreatGrandChild : greatGrandChild.children){
                        System.out.print(greatGreatGrandChild.value);
                        System.out.print(" ");
                    }
                    System.out.print("|");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");


    }
    
    private void printVTree4(){
        
        
        System.out.println(rootV.value);
        System.out.print(rootV.children.get(0).value);
        System.out.print("|");
        System.out.println(this.rootV.children.get(1).value);
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                System.out.print(grandChild.value);
                System.out.print(" ");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                for (SearchTreeNodeVolatile greatGrandChild: grandChild.children){
                    System.out.print(greatGrandChild.value);
                    System.out.print(" ");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                for (SearchTreeNodeVolatile greatGrandChild: grandChild.children){
                    for (SearchTreeNodeVolatile greatGreatGrandChild : greatGrandChild.children){
                        System.out.print(greatGreatGrandChild.value);
                        System.out.print(" ");
                    }
                    System.out.print("|");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");


    }
    
    
    
    private void printVTree4Bin(){
        
        
        System.out.println(rootV.sumValue);
        System.out.print(rootV.children.get(0).sumValue);
        System.out.print("|");
        System.out.println(this.rootV.children.get(1).sumValue);
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                System.out.print(grandChild.sumValue);
                System.out.print(" ");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                for (SearchTreeNodeVolatile greatGrandChild: grandChild.children){
                    System.out.print(greatGrandChild.sumValue);
                    System.out.print(" ");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");
        
        System.out.print("|");
        for (SearchTreeNodeVolatile child : rootV.children){
            for (SearchTreeNodeVolatile grandChild : child.children){
                for (SearchTreeNodeVolatile greatGrandChild: grandChild.children){
                    for (SearchTreeNodeVolatile greatGreatGrandChild : greatGrandChild.children){
                        System.out.print(greatGreatGrandChild.sumValue);
                        System.out.print(" ");
                    }
                    System.out.print("|");
                }
                System.out.print("|");
            }
            System.out.print("|");
        }
        System.out.println("");


    }
    
    
    public ArrayList linearSearchThreading(SearchTreeNodeVolatile node,double target,int noThreads) throws InterruptedException {
       //initialise globals
       
    
        ArrayList<double[]> listOfArrays = splitArray(node.children,noThreads);
       
        double[] sumArray = new double[noThreads];
        
        Thread[] sumThreads = new Thread[noThreads-1];
        SumArray[] sumers = new SumArray[noThreads-1];
        
        for (int i=0; i<noThreads-1; i=i+1){
            sumers[i] = new SumArray(listOfArrays.get(i));
            sumThreads[i] = new Thread(sumers[i]);
            sumThreads[i].start();
        }
        
        for (int i=0; i<noThreads-1; i=i+1){
            sumThreads[i].join();
        }
        
        double[] sums = new double[noThreads];
        sums[0] = 0;
        
        for (int i=1; i<noThreads; i=i+1){
            sums[i] = sumers[i-1].total;
        } 
        
               
        Thread[] searchThreads = new Thread[noThreads];
        ThreadLinearSearch[] linearSearches = new ThreadLinearSearch[noThreads];
        
        SharedVarsForSearch sharedVars = new SharedVarsForSearch();
        
        int totalAugment = 0;
        double currentSum = 0;
        
        for (int i=0; i<noThreads; i=i+1){
            
                       
            linearSearches[i] = new ThreadLinearSearch(sharedVars,listOfArrays.get(i),target,sums[i]+currentSum,totalAugment);
            
            searchThreads[i] = new Thread(linearSearches[i]);
            searchThreads[i].start();
            
            totalAugment = totalAugment+listOfArrays.get(i).length;
            currentSum = currentSum+sums[i];
        }
        
        for (int i=0; i<noThreads; i=i+1){
            searchThreads[i].join();
        }
        
        
        ArrayList retList = new ArrayList<>();
        
        
        retList.add(sharedVars.globalPointer);
        retList.add(sharedVars.globalSum);
        
        return(retList);
   
   }
    
    
    public int binarySearchThreading(SearchTreeNodeVolatile node,double target,int noThreads) throws InterruptedException {
       //initialise globals
       
       
       
        ArrayList<double[]> listOfArrays = splitArrayBinary(node.children,noThreads);
            
        Thread[] searchThreads = new Thread[noThreads];
        ThreadBinarySearch[] binarySearches = new ThreadBinarySearch[noThreads];
        
        SharedVarsForSearch sharedVars = new SharedVarsForSearch();
        
        int totalAugment = 0;
        double currentSum = 0;
        
        
        binarySearches[0] = new ThreadBinarySearch(sharedVars,listOfArrays.get(0),target,0,totalAugment);
            
        searchThreads[0] = new Thread(binarySearches[0]);
        searchThreads[0].start();
        
        totalAugment = listOfArrays.get(0).length;

        for (int i=1; i<noThreads; i=i+1){
            binarySearches[i] = new ThreadBinarySearch(sharedVars,listOfArrays.get(i),target,node.children.get(totalAugment-1).sumValue,totalAugment);
            
            searchThreads[i] = new Thread(binarySearches[i]);
            searchThreads[i].start();
            
            totalAugment = totalAugment+listOfArrays.get(i).length;
        }
        
        for (int i=0; i<noThreads; i=i+1){
            searchThreads[i].join();
        }
        
        
        
        return(sharedVars.globalPointer);
   
   }
    
    
   
   public static ArrayList splitArray(ArrayList<SearchTreeNodeVolatile> arrayToSplit, int noArrays){
       int arrayLength = arrayToSplit.size();
       int noExtras = arrayLength%noArrays;
       int baseLength = arrayLength/noArrays;
              
       ArrayList listOfArrays = new ArrayList<double[]>(); 
       
       for (int i =0; i<noArrays; i=i+1){
           double[] tempArray;
           if (i<noExtras){
               tempArray = new double[baseLength+1];
               for (int j=0; j<baseLength+1; j=j+1){
                   tempArray[j] = arrayToSplit.get(i*(baseLength+1)+j).value;
                   //System.out.println(tempArray[j]);
               }
           } else {
               tempArray = new double[baseLength];
               for (int j=0; j<baseLength; j=j+1){
                   tempArray[j] = arrayToSplit.get(noExtras*(baseLength+1)+(i-noExtras)*(baseLength)+j).value;
                   //System.out.println(tempArray[j]);
               }
           }
           //System.out.println("");
           listOfArrays.add(tempArray);
       }
       
       return(listOfArrays);
       
    }
   
   
   public static ArrayList splitArrayBinary(ArrayList<SearchTreeNodeVolatile> arrayToSplit, int noArrays){
       int arrayLength = arrayToSplit.size();
       int noExtras = arrayLength%noArrays;
       int baseLength = arrayLength/noArrays;
              
       ArrayList listOfArrays = new ArrayList<double[]>(); 
       
       for (int i =0; i<noArrays; i=i+1){
           double[] tempArray;
           if (i<noExtras){
               tempArray = new double[baseLength+1];
               for (int j=0; j<baseLength+1; j=j+1){
                   tempArray[j] = arrayToSplit.get(i*(baseLength+1)+j).sumValue;
                   //System.out.println(tempArray[j]);
               }
           } else {
               tempArray = new double[baseLength];
               for (int j=0; j<baseLength; j=j+1){
                   tempArray[j] = arrayToSplit.get(noExtras*(baseLength+1)+(i-noExtras)*(baseLength)+j).sumValue;
                   //System.out.println(tempArray[j]);
               }
           }
           //System.out.println("");
           listOfArrays.add(tempArray);
       }
       
       return(listOfArrays);
       
    }
   
   public static ArrayList splitArrayForNode(ArrayList<SearchTreeNodeVolatile> arrayToSplit, int noArrays){
       int arrayLength = arrayToSplit.size();
       int noExtras = arrayLength%noArrays;
       int baseLength = arrayLength/noArrays;
              
       ArrayList listOfArrays = new ArrayList<double[]>(); 
       
       for (int i =0; i<noArrays; i=i+1){
           SearchTreeNodeVolatile[] tempArray;
           if (i<noExtras){
               tempArray = new SearchTreeNodeVolatile[baseLength+1];
               for (int j=0; j<baseLength+1; j=j+1){
                   tempArray[j] = arrayToSplit.get(i*(baseLength+1)+j);
                   //System.out.println(tempArray[j]);
               }
           } else {
               tempArray = new SearchTreeNodeVolatile[baseLength];
               for (int j=0; j<baseLength; j=j+1){
                   tempArray[j] = arrayToSplit.get(noExtras*(baseLength+1)+(i-noExtras)*(baseLength)+j);
                   //System.out.println(tempArray[j]);
               }
           }
           //System.out.println("");
           listOfArrays.add(tempArray);
       }
       
       return(listOfArrays);
       
    }
        
        
   
    public void updatePropensitiesThreading(int noArrays, SearchTreeNodeVolatile root, int ruleType, int rule, int compartment, int fromCompartment, int toCompartment) throws InterruptedException{
        
            if (ruleType == 0) {
//                
//                for (Compartment comp : compartmentList){
//                    for (int type : comp.typeList){
//                        System.out.print(type);
//                        System.out.print(" ");
//                    }
//                    System.out.print(" | ");
//                }
//                System.out.println("");
//                
                
                intraRuleList[rule].executeRule(compartmentList[compartment]);
//                
//                for (Compartment comp : compartmentList){
//                    for (int type : comp.typeList){
//                        System.out.print(type);
//                        System.out.print(" ");
//                    }
//                    System.out.print(" | ");
//                }
//                System.out.println("");
//                
//                
                Thread[] threads = new Thread[noArrays];
                
                for (int i = 0; i<noCompartments; i=i+1){
                    for (int j = 0; j<(noCompartments-1); j=j+1){
                        
                        ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children.get(i).children.get(j).children,noArrays);
                        
                        int currentIndent = 0;
                        CalculatePropensityInter[] calculators = new CalculatePropensityInter[noArrays];
                        
                        for (int k = 0; k<noArrays; k=k+1){
                            calculators[k] = new CalculatePropensityInter(childrenToUpdate.get(k),currentIndent,i,j,interRuleList,interFuncts,compartmentList);
                            threads[k] = new Thread(calculators[k]);
                            threads[k].run();
                            currentIndent = currentIndent + childrenToUpdate.get(k).length;
                        }
                        
                        for (int k = 0; k<noArrays; k=k+1){
                            threads[k].join();
                        }          
                        
                        
                        
                    }
                    
                    ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children.get(i).children,noArrays);
                        
                    SumChildren[] updators = new SumChildren[noArrays];
                    
                    for (int j = 0; j<noArrays; j=j+1){
                        updators[j] = new SumChildren(childrenToUpdate.get(j));
                        threads[j] = new Thread(updators[j]);
                        threads[j].run();
                    }

                    for (int j = 0; j<noArrays; j=j+1){
                        threads[j].join();
                    }
                    
                }
                
                
                ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children,noArrays);
                        
                SumChildren[] updators = new SumChildren[noArrays];

                for (int i = 0; i<noArrays; i=i+1){
                    updators[i] = new SumChildren(childrenToUpdate.get(i));
                    threads[i] = new Thread(updators[i]);
                    threads[i].run();
                }

                for (int i = 0; i<noArrays; i=i+1){
                    threads[i].join();
                }
                    

                
                for (int i=0; i<noCompartments; i=i+1){
                        
                    childrenToUpdate = splitArrayForNode(root.children.get(0).children.get(i).children,noArrays);

                    int currentIndent = 0;
                    CalculatePropensityIntra[] calculators = new CalculatePropensityIntra[noArrays];

                    for (int j = 0; j<noArrays; j=j+1){
                        calculators[j] = new CalculatePropensityIntra(childrenToUpdate.get(j),currentIndent,i,intraRuleList,intraFuncts,compartmentList);
                        threads[j] = new Thread(calculators[j]);
                        threads[j].run();
                        currentIndent = currentIndent + childrenToUpdate.get(j).length;
                    }

                    for (int j = 0; j<noArrays; j=j+1){
                        threads[j].join();
                    }

                    

                }
                
                childrenToUpdate = splitArrayForNode(root.children.get(0).children,noArrays);

                updators = new SumChildren[noArrays];

                for (int j = 0; j<noArrays; j=j+1){
                    updators[j] = new SumChildren(childrenToUpdate.get(j));
                    threads[j] = new Thread(updators[j]);
                    threads[j].run();
                }

                for (int j = 0; j<noArrays; j=j+1){
                    threads[j].join();
                }
                
                threads[0] = new Thread( new SumChildren(new SearchTreeNodeVolatile[]{root.children.get(0)}));
                threads[0].start();
                threads[1] = new Thread( new SumChildren(new SearchTreeNodeVolatile[]{root.children.get(1)}));
                threads[1].start();
                
                threads[0].join();
                threads[1].join();
                
                root.value = root.children.get(0).value + root.children.get(1).value;

                
                //root.updateTreeValues();
            
            } else {
                if (fromCompartment <= toCompartment){
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment+1]);
                } else {
                    interRuleList[rule].executeRule(compartmentList[fromCompartment],compartmentList[toCompartment]);
                }
                                
                Thread[] threads = new Thread[noArrays];
                
                for (int i = 0; i<noCompartments; i=i+1){
                    for (int j = 0; j<(noCompartments-1); j=j+1){
                        
                        ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children.get(i).children.get(j).children,noArrays);
                        
                        int currentIndent = 0;
                        CalculatePropensityInter[] calculators = new CalculatePropensityInter[noArrays];
                        
                        for (int k = 0; k<noArrays; k=k+1){
                            calculators[k] = new CalculatePropensityInter(childrenToUpdate.get(k),currentIndent,i,j,interRuleList,interFuncts,compartmentList);
                            threads[k] = new Thread(calculators[k]);
                            threads[k].run();
                            currentIndent = currentIndent + childrenToUpdate.get(k).length;
                        }
                        
                        for (int k = 0; k<noArrays; k=k+1){
                            threads[k].join();
                        }          
                        
                        
                        
                    }
                    
                    ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children.get(i).children,noArrays);
                        
                    SumChildren[] updators = new SumChildren[noArrays];
                    
                    for (int j = 0; j<noArrays; j=j+1){
                        updators[j] = new SumChildren(childrenToUpdate.get(j));
                        threads[j] = new Thread(updators[j]);
                        threads[j].run();
                    }

                    for (int j = 0; j<noArrays; j=j+1){
                        threads[j].join();
                    }
                    
                }
                
                
                ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(root.children.get(1).children,noArrays);
                        
                SumChildren[] updators = new SumChildren[noArrays];

                for (int i = 0; i<noArrays; i=i+1){
                    updators[i] = new SumChildren(childrenToUpdate.get(i));
                    threads[i] = new Thread(updators[i]);
                    threads[i].run();
                }

                for (int i = 0; i<noArrays; i=i+1){
                    threads[i].join();
                }
                    

                
                for (int i=0; i<noCompartments; i=i+1){
                        
                    childrenToUpdate = splitArrayForNode(root.children.get(0).children.get(i).children,noArrays);

                    int currentIndent = 0;
                    CalculatePropensityIntra[] calculators = new CalculatePropensityIntra[noArrays];

                    for (int j = 0; j<noArrays; j=j+1){
                        calculators[j] = new CalculatePropensityIntra(childrenToUpdate.get(j),currentIndent,i,intraRuleList,intraFuncts,compartmentList);
                        threads[j] = new Thread(calculators[j]);
                        threads[j].run();
                        currentIndent = currentIndent + childrenToUpdate.get(j).length;
                    }

                    for (int j = 0; j<noArrays; j=j+1){
                        threads[j].join();
                    }

                    

                }
                
                childrenToUpdate = splitArrayForNode(root.children.get(0).children,noArrays);

                updators = new SumChildren[noArrays];

                for (int j = 0; j<noArrays; j=j+1){
                    updators[j] = new SumChildren(childrenToUpdate.get(j));
                    threads[j] = new Thread(updators[j]);
                    threads[j].run();
                }

                for (int j = 0; j<noArrays; j=j+1){
                    threads[j].join();
                }

                threads[0] = new Thread( new SumChildren(new SearchTreeNodeVolatile[]{root.children.get(0)}));
                threads[0].start();
                threads[1] = new Thread( new SumChildren(new SearchTreeNodeVolatile[]{root.children.get(1)}));
                threads[1].start();
                
                threads[0].join();
                threads[1].join();
                
                root.value = root.children.get(0).value + root.children.get(1).value;
                                
            }
            
    }
    
    private void updateNodesThreadingInter(int noArrays,int compartment) throws InterruptedException{
        
        ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(rootV.children.get(1).children.get(compartment).children,noArrays);
                
        Thread[] threads = new Thread[noArrays];
        
        StrongUpdatorInter[] updators = new StrongUpdatorInter[noArrays];
        
        
        double oldSum3 = rootV.children.get(1).children.get(compartment).value;
        double oldSum4 = rootV.children.get(1).value;
        
        double totalDifference = 0;
        
        int index = 0;
        for (int i=0; i<noArrays; i++){
            
            updators[i] = new StrongUpdatorInter(childrenToUpdate.get(i),interRuleList,compartmentList,interFuncts,compartment,index);
            threads[i] = new Thread(updators[i]);
            threads[i].run();
            index = index+childrenToUpdate.get(i).length;
            
        }

        for (int j = 0; j<noArrays; j=j+1){
            threads[j].join();
        }
        
        for (int j = 0; j<noArrays; j=j+1){
            totalDifference = totalDifference+updators[j].difference;
        }
        
        rootV.children.get(1).children.get(compartment).value = rootV.children.get(1).children.get(compartment).value + totalDifference;
        rootV.children.get(1).updateSumFromOneChild(compartment,oldSum3);
        rootV.updateSumFromOneChild(1,oldSum4);
        

    }
        
    private void updateNodesThreadingIntra(int noArrays,int compartment) throws InterruptedException{
        
        ArrayList<SearchTreeNodeVolatile[]> childrenToUpdate = splitArrayForNode(rootV.children.get(0).children.get(compartment).children,noArrays);
        
        Thread[] threads = new Thread[noArrays];
        
        StrongUpdatorIntra[] updators = new StrongUpdatorIntra[noArrays];
        
        
        double oldSum1 = rootV.children.get(0).value;
        double oldSum2 = rootV.children.get(0).children.get(compartment).value;
        
        
        int index = 0;
        for (int i=0; i<noArrays; i++){
            
            updators[i] = new StrongUpdatorIntra(childrenToUpdate.get(i),intraRuleList,compartmentList,intraFuncts,compartment,index);
            threads[i] = new Thread(updators[i]);
            threads[i].run();
            index = index+childrenToUpdate.get(i).length;
            System.out.println(index);
        }

        for (int j = 0; j<noArrays; j=j+1){
            threads[j].join();
        }
        
        double total = 0;
        for (int j = 0; j<noArrays; j=j+1){
            total = total+ updators[j].total;
        }
        
        rootV.children.get(0).children.get(compartment).value = total;
        rootV.children.get(0).updateSumFromOneChild(compartment, oldSum2);
        rootV.updateSumFromOneChild(0,oldSum1);
        

    }
    
    private int binarySearch(double target,SearchTreeNode node){
        
        int noChildren = node.children.size();
        
        int currentPointer = (int) Math.floor(noChildren/2);
        boolean found = false;
        int lowIndex = 0;
        int highIndex = noChildren-1;
            
        while (!(found)){

            if (currentPointer==0){
                if ((0 < target) &&( target <= node.children.get(currentPointer).sumValue)){
                    found = true;
                } else if ((node.children.get(currentPointer).sumValue < target) && (target <= node.children.get(currentPointer+1).sumValue)){
                    currentPointer = currentPointer+1;
                    found = true;
                } else {
                    System.out.println("error");
                }
            }
            if (highIndex-lowIndex < 2){
                if ((node.children.get(lowIndex).sumValue <= target) && (target <= node.children.get(lowIndex+1).sumValue)){
                    found = true;
                    currentPointer = lowIndex+1;
                } else {
                    found = true;
                    currentPointer = lowIndex;
                }
            } else {
                if ((node.children.get(currentPointer-1).sumValue < target) && (target <= node.children.get(currentPointer).sumValue)){
                    found = true;
                } else if (target <= node.children.get(currentPointer-1).sumValue) {
                    highIndex = currentPointer-1;
                    currentPointer = (int) (lowIndex+Math.floor((highIndex-lowIndex)/2));
                } else{
                    lowIndex = currentPointer;
                    currentPointer = (int) (lowIndex+Math.floor((highIndex-lowIndex)/2));
                }
            }
        }
        
        return(currentPointer);
    }
    
    
}
