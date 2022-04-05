import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.io.IOException;
import java.util.ArrayList;
import javax.swing.JFrame;  
import javax.swing.JPanel;
import javax.swing.SwingUtilities;  
import javax.swing.WindowConstants;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;


public class NewMain {

    
    public static void main(String[] args) throws InterruptedException, IOException{    

        
        //This java program runs the same algorithm as the python code I provided
        //with the added benefit of including a hyperthreading option for varients
        //of the algorithm (but not the same one I described in my dissertation,
        //rather a different idea altogether that I implemented for URSS)
        
        //this file is currently configured to run the experement to test
        //intercompartmental R_0
        
        Maths M = new Maths();
        
        //System.out.println(M.nCr(170,15));
        //System.out.println(M.nCr(170, 1));
        
        
        
//        Compartment comp0 = new Compartment(new int[]{1495,5,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][] {{0.0002,0.0002},{0.0002,0.0002},{0.0002,0.0002}});
//        Compartment comp1 = new Compartment(new int[]{1495,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][] {{0.0002,0.0002},{0.0002,0.0002},{0.0002,0.0002}});
//        Compartment comp2 = new Compartment(new int[]{1495,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][] {{0.0002,0.0002},{0.0002,0.0002},{0.0002,0.0002}});
        
        //Compartment[] comps = new Compartment[]{comp0,comp1,comp2};
        

        //Compartment[] comps = new Compartment[]{comp0};
        
        
        //IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,1,0},new int[]{1,0,0,0}, M)};
        //InterRule[] interRuleList = new InterRule[]{new InterRule(new int[]{1,0,0,0},new int[]{1,0,0,0},M),new InterRule(new int[]{0,1,0,0},new int[]{0,1,0,0},M),new InterRule(new int[]{0,0,1,0},new int[]{0,0,1,0},M)};
        //Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};
        //Funct[] interFuncts = new Funct[]{new Constant(), new Constant(), new Constant()};
        
//        
//        IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,0,1},new int[]{1,0,0,0}, M)};
//        InterRule[] interRuleList = new InterRule[]{};
//        Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};
//        Funct[] interFuncts = new Funct[]{};
//        
        //======================================================old working^ new diffusion below=========================================

        //InterRule[] interRuleList = new InterRule[]{new InterRule(new int[]{1},new int[]{1},M),new InterRule(new int[]{1},new int[]{1},M),new InterRule(new int[]{1},new int[]{1},M),new InterRule(new int[]{1},new int[]{1},M)};
        
//        
//        Funct[] interFuncts = new Funct[8*8*4+4*8*3+4*2];
          //Funct[] interFuncts = new Funct[]{new Constant(),new Constant(),new Constant(),new Constant()};
//        
//        double[][] passing = new double[8*8*4+4*8*3+4*2][99];
//        for (int i=0; i<8*8*4+4*8*3+4*2; i++){
//            for (int j=0; j<99; j++){
//                passing[i][j]=1;
//            }
//        }
//        

//        Compartment[] comps = new Compartment[100];
////        comps[0] = new Compartment(new int[]{200}, new double[]{}, passing);
////        for (int i=1; i<100; i++){
////            comps[i] = new Compartment(new int[]{0}, new double[]{}, passing);
////        }
//        
//        IntraRule[] intraRuleList = new IntraRule[]{};
//        Funct[] intraFuncts = new Funct[]{};
//        InterRule[] interRuleList = new InterRule[4];
//        Funct[] interFuncts = new Funct[4];
//        
//        for (int i = 0; i<4; i++){
//            interRuleList[i] = new InterRule(new int[]{1}, new int[]{1},M);
//            interFuncts[i] = new Constant();
//        }
//        
//        int count = 0;
//        for (int i=0; i<10; i++){
//            for (int j=0; j<10; j++){
//                
//                if ((i==0)&&(j==0)){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    //up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    //left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
//                    
//                    comps[i*10+j] = new Compartment(new int[]{200},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if ((i==9)&&(j==0)){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    //down[i*10+j+9]=1;
//                    //left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
//                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if ((i==0)&&(j==9)){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    //up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    //right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
////                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if ((i==9)&&(j==9)){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    //down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    //right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
////                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if (i==0){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    //up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
////                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if (i==9){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    //down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
//                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//                else if (j==9){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    //right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
////                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                else if (j==0){
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    //left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
//                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                } else {
//                    double[] up = new double[99];
//                    double[] down = new double[99];
//                    double[] left = new double[99];
//                    double[] right = new double[99];
//                    for (int k=0; k<99; k++){
//                        up[k]=0;
//                        down[k]=0;
//                        left[k]=0;
//                        right[k]=0;
//                    }
//                    up[i*10+j-10]=1;
//                    down[i*10+j+9]=1;
//                    left[i*10+j-1]=1;
//                    right[i*10+j]=1;
////                    
////                    double[][] passingParam = new double[99][4];
////                    
////                    for (int a=0; a<99; a++){
////                        for (int b=0; b<4; b++){
////                            passingParam[a][b]=0;
////                        }
////                    }
////                    
////                    for (int a=0; a<99; a++){
////                        if(up[a]==1){
////                            passingParam[a][0]=1;
////                        }
////                        if(down[a]==1){
////                            passingParam[a][1]=1;
////                        }
////                        if(left[a]==1){
////                            passingParam[a][2]=1;
////                        }
////                        if(right[a]==1){
////                            passingParam[a][3]=1;
////                        }
////                    }
//                    
//                    comps[i*10+j] = new Compartment(new int[]{0},new double[]{},new double[][]{up,down,left,right});
//                }
//                
//            }
//        }
//        System.out.println(count);
//
//        Gillespie gil = new Gillespie(comps,intraRuleList,interRuleList,500,250000,intraFuncts,interFuncts);
//        
//        gil.runLinearStrong();
//        
//        


//    =============================================  Grid structure below    ===========================================

//        IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,1,0},new int[]{1,0,0,0}, M)};
//        
//        Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};
//        
//        
//        double transportRate  = 0.0002;
//
//        InterRule[] interRuleList = new InterRule[4*3];
//        Funct[] interFuncts = new Funct[4*3];
//        
//        Compartment[] comps = new Compartment[100];
//        
//        for (int i = 0; i<4; i++){
//            interRuleList[i*3] = new InterRule(new int[]{1,0,0,0}, new int[]{1,0,0,0},M);
//            interFuncts[i*3] = new Constant();
//            interRuleList[i*3+1] = new InterRule(new int[]{0,1,0,0}, new int[]{0,1,0,0},M);
//            interFuncts[i*3+1] = new Constant();
//            interRuleList[i*3+2] = new InterRule(new int[]{0,0,1,0}, new int[]{0,0,1,0},M);
//            interFuncts[i*3+2] = new Constant();
//        }
//        
//        int count = 0;
//        for (int i=0; i<10; i++){
//            for (int j=0; j<10; j++){
//                
//                if ((i==0)&&(j==0)){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    downS[i*10+j+9]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    
//                    comps[i*10+j] = new Compartment(new int[]{45,5,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if ((i==9)&&(j==0)){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if ((i==0)&&(j==9)){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    
//                    downS[i*10+j+9]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    
//  
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if ((i==9)&&(j==9)){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if (i==0){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    
//                    downS[i*10+j+9]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if (i==9){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//                else if (j==9){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    downS[i*10+j+9]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                else if (j==0){
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    downS[i*10+j+9]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                } else {
//                    double[] upS = new double[99];
//                    double[] downS = new double[99];
//                    double[] leftS = new double[99];
//                    double[] rightS = new double[99];
//                    double[] upI = new double[99];
//                    double[] downI = new double[99];
//                    double[] leftI = new double[99];
//                    double[] rightI = new double[99];
//                    double[] upR = new double[99];
//                    double[] downR = new double[99];
//                    double[] leftR = new double[99];
//                    double[] rightR = new double[99];
//                    for (int k=0; k<99; k++){
//                        upS[k]=0;
//                        downS[k]=0;
//                        leftS[k]=0;
//                        rightS[k]=0;
//                        upI[k]=0;
//                        downI[k]=0;
//                        leftI[k]=0;
//                        rightI[k]=0;
//                        upR[k]=0;
//                        downR[k]=0;
//                        leftR[k]=0;
//                        rightR[k]=0;
//                    }
//                    upS[i*10+j-10]=transportRate;
//                    upI[i*10+j-10]=transportRate;
//                    upR[i*10+j-10]=transportRate;
//                    downS[i*10+j+9]=transportRate;
//                    downI[i*10+j+9]=transportRate;
//                    downR[i*10+j+9]=transportRate;
//                    leftS[i*10+j-1]=transportRate;
//                    leftI[i*10+j-1]=transportRate;
//                    leftR[i*10+j-1]=transportRate;
//                    rightS[i*10+j]=transportRate;
//                    rightI[i*10+j]=transportRate;
//                    rightR[i*10+j]=transportRate;
//
//                    
//                    comps[i*10+j] = new Compartment(new int[]{50,0,0,0}, new double[]{0.5,0.07,0.02,0.005},new double[][]{upS,upI,upR,downS,downI,downR,leftS,leftI,leftR,rightS,rightI,rightR});
//                }
//                
//            }
//        }
//        System.out.println(count);
//
//        Gillespie gil = new Gillespie(comps,intraRuleList,interRuleList,500,250000,intraFuncts,interFuncts);
//        
//        gil.runLinearStrong();
        
        
//    =============================================  Complete graph below  ===========================================

        double averageEndemic = 0;
        int successes = 0;
        

        for (int itteration=0;itteration<1000;itteration++){
            System.out.println(itteration);


            IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,1,0},new int[]{1,0,0,0}, M)};

            Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};

            //R_0 = 0.1
            //double transportRate  = 1.826771487/10000000;
            //R_0 = 0.5
            //double transportRate  = 9.159718945/10000000;
            //R_0 = 0.9
            //double transportRate  = 1.653435477/1000000;
            //R_0 = 1
            //double transportRate  = 1.8388457641/1000000;
            //R_0 = 2
            //double transportRate  = 3.703299382/1000000;
            //R_0 = 5
            double transportRate  = 9.462976738/1000000;
            //R_0 = 49.5
            //double transportRate  = 1.451701302/1000;
            InterRule[] interRuleList = new InterRule[3];
            Funct[] interFuncts = new Funct[3];

            Compartment[] comps = new Compartment[100];

            for (int i = 0; i<1; i++){
                interRuleList[i*3] = new InterRule(new int[]{1,0,0,0}, new int[]{1,0,0,0},M);
                interFuncts[i*3] = new Constant();
                interRuleList[i*3+1] = new InterRule(new int[]{0,1,0,0}, new int[]{0,1,0,0},M);
                interFuncts[i*3+1] = new Constant();
                interRuleList[i*3+2] = new InterRule(new int[]{0,0,1,0}, new int[]{0,0,1,0},M);
                interFuncts[i*3+2] = new Constant();
            }

            int count = 0;
            for (int i=0; i<10; i++){
                for (int j=0; j<10; j++){

                    if ((i==0)&&(j==0)){
                        double[] upS = new double[99];
                        double[] downS = new double[99];
                        double[] leftS = new double[99];
                        double[] rightS = new double[99];
                        double[] upI = new double[99];
                        double[] downI = new double[99];
                        double[] leftI = new double[99];
                        double[] rightI = new double[99];
                        double[] upR = new double[99];
                        double[] downR = new double[99];
                        double[] leftR = new double[99];
                        double[] rightR = new double[99];
                        for (int k=0; k<99; k++){
                            upS[k]=transportRate;
                            downS[k]=transportRate;
                            leftS[k]=transportRate;
                            rightS[k]=transportRate;
                            upI[k]=transportRate;
                            downI[k]=transportRate;
                            leftI[k]=transportRate;
                            rightI[k]=transportRate;
                            upR[k]=transportRate;
                            downR[k]=transportRate;
                            leftR[k]=transportRate;
                            rightR[k]=transportRate;
                        }

                        comps[i*10+j] = new Compartment(new int[]{495,5,0,0}, new double[]{0.5,0.07,0.02,0.00},new double[][]{upS,upI,upR});

                    } else {
                        double[] upS = new double[99];
                        double[] downS = new double[99];
                        double[] leftS = new double[99];
                        double[] rightS = new double[99];
                        double[] upI = new double[99];
                        double[] downI = new double[99];
                        double[] leftI = new double[99];
                        double[] rightI = new double[99];
                        double[] upR = new double[99];
                        double[] downR = new double[99];
                        double[] leftR = new double[99];
                        double[] rightR = new double[99];
                        for (int k=0; k<99; k++){
                            upS[k]=transportRate;
                            downS[k]=transportRate;
                            leftS[k]=transportRate;
                            rightS[k]=transportRate;
                            upI[k]=transportRate;
                            downI[k]=transportRate;
                            leftI[k]=transportRate;
                            rightI[k]=transportRate;
                            upR[k]=transportRate;
                            downR[k]=transportRate;
                            leftR[k]=transportRate;
                            rightR[k]=transportRate;
                        }

                        comps[i*10+j] = new Compartment(new int[]{500,0,0,0}, new double[]{0.5,0.07,0.02,0.00},new double[][]{upS,upI,upR});
                    }

                }
            }
            System.out.println(count);

            Gillespie gil = new Gillespie(comps,intraRuleList,interRuleList,100000,1000000,intraFuncts,interFuncts);

            int[] result = gil.runLinearStrong();

            int total = 0;
            for (int a=0; a<100; a++){
                //System.out.println(result[a]);
                total = total+result[a];
            }
            
            if (result[100] == 0) {
                averageEndemic = averageEndemic+total;
                successes = successes+1;
                System.out.println("success");
                System.out.println(result[100]);
                System.out.println(averageEndemic/successes);
            } else {
                averageEndemic = averageEndemic+total;
                successes = successes+1;
                System.out.print("faliure ");
                System.out.println(result[100]);
                System.out.println(averageEndemic/successes);
            }
            
            
        }
        
        System.out.println(averageEndemic/successes);
        
        //    =============================================  Chain structure below    ===========================================
////
//        int total=0;
//        for (int counter=0; counter<1000; counter++){
//        IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,1,0},new int[]{1,0,0,0}, M)};
//        
//        Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};
//        
//        
//        double transportRate  = 0.09/(2*850);
//
//        InterRule[] interRuleList = new InterRule[2*3];
//        Funct[] interFuncts = new Funct[2*3];
//        
//        Compartment[] comps = new Compartment[10];
//        
//        for (int i = 0; i<2; i++){
//            interRuleList[i*3] = new InterRule(new int[]{1,0,0,0}, new int[]{1,0,0,0},M);
//            interFuncts[i*3] = new Constant();
//            interRuleList[i*3+1] = new InterRule(new int[]{0,1,0,0}, new int[]{0,1,0,0},M);
//            interFuncts[i*3+1] = new Constant();
//            interRuleList[i*3+2] = new InterRule(new int[]{0,0,1,0}, new int[]{0,0,1,0},M);
//            interFuncts[i*3+2] = new Constant();
//        }
//        
//        int count = 0;
//        for (int i=0; i<10; i++){
//            //System.out.println("here");
//                
//            if (i==0){
//                double[] leftS = new double[9];
//                double[] rightS = new double[9];
//                double[] leftI = new double[9];
//                double[] rightI = new double[9];
//                double[] leftR = new double[9];
//                double[] rightR = new double[9];
//                for (int k=0; k<9; k++){
//                    leftS[k]=0;
//                    rightS[k]=0;
//                    leftI[k]=0;
//                    rightI[k]=0;
//                    leftR[k]=0;
//                    rightR[k]=0;
//                    
//                }
//                
//                rightS[i]=transportRate;
//                
//                rightI[i]=transportRate;
//                
//                rightR[i]=transportRate;
//
//                
//                comps[i] = new Compartment(new int[]{995,5,0,0}, new double[]{0.2,0.07,0.02,0.00},new double[][]{leftS,leftI,leftR,rightS,rightI,rightR});
//            }
//                
//            else if (i==9){
//                
//                double[] leftS = new double[9];
//                double[] rightS = new double[9];
//                
//                double[] leftI = new double[9];
//                double[] rightI = new double[9];
//                
//                double[] leftR = new double[9];
//                double[] rightR = new double[9];
//                
//                for (int k=0; k<9; k++){
//                    
//                    leftS[k]=0;
//                    rightS[k]=0;
//                    leftI[k]=0;
//                    rightI[k]=0;
//                    leftR[k]=0;
//                    rightR[k]=0;
//                }
//                leftS[8]=transportRate;
//                leftI[8]=transportRate;
//                leftR[8]=transportRate;
//                
//                
//
//
//                comps[i] = new Compartment(new int[]{1000,0,0,0}, new double[]{0.2,0.07,0.02,0.00},new double[][]{leftS,leftI,leftR,rightS,rightI,rightR});
//            
//            } else {
//                double[] leftS = new double[9];
//                double[] rightS = new double[9];
//                double[] leftI = new double[9];
//                double[] rightI = new double[9];
//                double[] leftR = new double[9];
//                double[] rightR = new double[9];
//                for (int k=0; k<9; k++){
//                    leftS[k]=0;
//                    rightS[k]=0;
//                    leftI[k]=0;
//                    rightI[k]=0;
//                    leftR[k]=0;
//                    rightR[k]=0;
//                }
//                leftS[i-1]=transportRate;
//                leftI[i-1]=transportRate;
//                leftR[i-1]=transportRate;
//                rightS[i]=transportRate;
//                rightI[i]=transportRate;
//                rightR[i]=transportRate;   
//                
//
//                comps[i] = new Compartment(new int[]{1000,0,0,0}, new double[]{0.2,0.07,0.02,0.00},new double[][]{leftS,leftI,leftR,rightS,rightI,rightR});
//            }
//
//            
//        }
//        
//        
//
//        Gillespie gil = new Gillespie(comps,intraRuleList,interRuleList,1000,250000,intraFuncts,interFuncts);
//        
//        int flag = gil.runLinearStrong();
//        total = total+flag;
//        System.out.println(counter);
//
//    }
//        System.out.println(total);
        
        
//        
//        // two compartments
//        int total=0;
//        for (int counter=0; counter<100; counter++){
//        IntraRule[] intraRuleList = new IntraRule[]{new IntraRule(new int[]{1,1,0,0},new int[]{0,2,0,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,1,0}, M),new IntraRule(new int[]{0,1,0,0},new int[]{0,0,0,1}, M),new IntraRule(new int[]{0,0,1,0},new int[]{1,0,0,0}, M)};
//        
//        Funct[] intraFuncts = new Funct[]{new ConstantDivPop(), new Constant(), new Constant(), new Constant()};
//        
//        
//        double transportRate  = 0.09/(2790);
//
//        InterRule[] interRuleList = new InterRule[2];
//        Funct[] interFuncts = new Funct[2];
//        
//        Compartment[] comps = new Compartment[2];
//        
//        for (int i = 0; i<2; i++){
//
//            interRuleList[i] = new InterRule(new int[]{0,1,0,0}, new int[]{0,1,0,0},M);
//            interFuncts[i] = new Constant();
//
//        }
//        
//        System.out.println(interFuncts[0]);
//        System.out.println(interFuncts[1]);
//        
//        int count = 0;
//        for (int i=0; i<3; i++){
//            System.out.print("i");
//            System.out.println(i);
//                
//            if (i==0){
//                double[] leftI = new double[1];
//                double[] rightI = new double[1];
//                for (int k=0; k<1; k++){
//                    leftI[k]=0;
//                    rightI[k]=0;
//                    
//                }
//                
//                
//                
//                rightI[i]=transportRate;
//                
//                
//
//                
//                comps[i] = new Compartment(new int[]{2995,5,0,0}, new double[]{0.2,0.07,0.02,0.00},new double[][]{leftI,rightI});
//            }
//                
//            else if (i==1){
//                
//                System.out.println("here");
//            
//                
//                double[] leftI = new double[1];
//                double[] rightI = new double[1];
//                
//                
//                for (int k=0; k<1; k++){
//                    
//                    leftI[k]=0;
//                    rightI[k]=0;
//                    
//                }
//                
//                leftI[0]=transportRate;
//                
//                
//                
//
//
//                comps[i] = new Compartment(new int[]{3000,0,0,0}, new double[]{0.2,0.07,0.02,0.00},new double[][]{leftI,rightI});
//            
//
//            
//        }
//            
//        }
//        
//        
//        System.out.println(comps[1]);
//        Gillespie gil = new Gillespie(comps,intraRuleList,interRuleList,1000,250000,intraFuncts,interFuncts);
//        
//        int flag = gil.runLinearStrong();
//        total = total+flag;
//        System.out.println(counter);
//        }
//    
//        System.out.println(total);
//        
        
//        
        //Can't remember what is below but not important to what is above
        
        
//======================================================================================================        
        
        
        
//        //gil.runBinaryThreading(2);
//        ArrayList returnedData = gil.runLinearThreading(2);
//        //396
//        
//        double[][][] realData = (double[][][]) returnedData.get(0);
//        double[] timeData = (double[]) returnedData.get(1);
//        
//        
//        
//        for (int k=0; k<comps.length ;k++){
//
//            XYSeries[] lines = new XYSeries[((int) realData[1].length)];
//
//            for (int i=0; i<((int) realData[1].length); i++){
//                lines[i] = new XYSeries( "Type"+i );
//            }
//
//            for (int i = 0; i < (int) returnedData.get(2); i++){
//
//                for (int j = 0; j < ((int) realData[1].length); j++){
//                    lines[j].add(timeData[i],realData[i][j][k]);
//                    //System.out.println(realData[i][j][k]);
//                }
//            } 
//
//
//            XYSeriesCollection dataset = new XYSeriesCollection(); 
//
//            for (int i=0; i<((int) realData[1].length); i++){
//                dataset.addSeries(lines[i]);
//            }
//
//            String title = (String) ("Compartment"+k);
//            
//            new XYLineChartExample(dataset,title).setVisible(true);
//      }
    
        
    }
}
        

        
      // Create dataset

    // Create chart
//    JFreeChart chart = ChartFactory.createXYLineChart("test","t", "r", dataset);
// 
//    Global thing;
//    ChartPanel thing = new ChartPanel(chart);
//    //setContentPanel(panel);
//    JPanel chartPanel = new ChartPanel(chart);
//    chartPanel.setSize(640, 480);
//    
//    
//    public XYLineChartExample() {
// 
//        JPanel chartPanel = thing;
//        add(chartPanel, BorderLayout.CENTER);
// 
//        setSize(640, 480);
//        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//        setLocationRelativeTo(null);
//    }
//       
//    }
    

