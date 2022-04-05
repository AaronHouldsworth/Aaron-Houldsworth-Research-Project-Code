#This file contains the neccecary code to run simulations for a 
#multicompartmental SIRD model where we assume the kinetic functions are
#constant

#import neccecary libraries
import numpy as np
import matplotlib.pyplot as plt
import time

#define functions to be used later
def factorial(n):
    if n==1 or n==0:
        return(1)
    else:
        return(n*factorial(n-1))

def ncr(n,r):
    if r>n:
        return(0)
    elif n==0 and r==0:
        return(1)
    elif r==0:
        return(1)
    elif r==1:
        return(n)
    elif r==2:
        return(n*(n-1)/2)
    else:
        return(factorial(n)/(factorial(r)*factorial(n-r)))

#define classes used in HKO tree construction
class Node:

    def __init__(self,propensity):
        
        self.partSum = propensity
        self.childeren = []
        #self.coord = coord

    def addChild(self,childNode):

        self.childeren.append(childNode)
        #self.updatePartSum()


    def getPartSum(self):
        return(self.partSum)

    
   
    def updatePartSum(self):

        if self.childeren != []:
            total = 0

            for child in self.childeren:
                total = total+child.updatePartSum()

            self.partSum = total
            

        return(self.partSum)

    def updatePartSumFromOneChild(self,childLocation,oldChildSum):

        self.partSum = self.partSum - oldChildSum + self.childeren[childLocation].partSum

    def adjustPropensityForLeaf(self,newProp):

        self.partSum = newProp

    def getSubTree(self):
        data = []

        
        for child in self.childeren:
            #print(child.partSum, end = '')
            data.append(child.getSubTree())
        #print("")

        return([self.partSum,data])
        #return(self.partSum)

    def printSubTree(self):

        for child in self.childeren:
            print(child.partSum, end='')
        print("\n",self.partSum)

        print(self.partSum)

        for child in self.childeren:
            child.printSubTree()


#Define classes for rules
class intraRule:

    def __init__(self,sourceComplex,targetComplex,kineticFunct):
        self.sourceComplex = sourceComplex
        self.targetComplex = targetComplex
        self.kineticFunct = kineticFunct
        self.kineticConst = 0

    def executeRule(self,compartment):
        for i in range(0,compartment.noTypes):
            compartment.typeList[i] = compartment.typeList[i] - self.sourceComplex[i] + self.targetComplex[i]

    def calculatePropensity(self,compartment):
        total = self.kineticConst
        for i in range(0,compartment.noTypes):
            total = total*(ncr(compartment.typeList[i],self.sourceComplex[i]))

        return(total)
            


class interRule:

    def __init__(self,sourceComplex,targetComplex,kineticFunct):
        self.sourceComplex = sourceComplex
        self.targetComplex = targetComplex
        self.kineticFunct = kineticFunct
        self.kineticConst = 0

    def executeRule(self,sourceCompartment,targetCompartment):
        for i in range(0,sourceCompartment.noTypes):
            #print(sourceCompartment.typeList[i] - self.sourceComplex[i])
            sourceCompartment.typeList[i] = sourceCompartment.typeList[i] - self.sourceComplex[i]
            #print("moveing ", self.sourceComplex[i] ,"of type ",i)
            #print(targetCompartment.typeList[i] + self.targetComplex[i])
            targetCompartment.typeList[i] = targetCompartment.typeList[i] + self.targetComplex[i]

    def calculatePropensity(self,compartment):
        total = self.kineticConst
        #print(total)
        
        for i in range(0,compartment.noTypes):
            total = total*(ncr(compartment.typeList[i],self.sourceComplex[i]))
            #print("placeholder")
            #print(total)

        return(total)
    
    

#define class for compartment
class compartment:
    def __init__(self,typeList,intraParams,interParams):

        self.typeList = typeList
        self.noTypes = len(typeList)
        self.intraParams = intraParams
        self.interParams = interParams
        self.initPop = self.getPopulation()
        
    def getPopulation(self):
        total = 0
        for type in self.typeList:
            total = total+type
            
        return(total)
        




#define kinetic functions. These should be substituted into the instances
#of rules we create later. These functions are modified as appropriate 
#to implement different varients of the functions
def const(x,compartment,compartment2,compartmentList):
    return(x)

def constDivPop(x,compartment,compartment2,compartmentList):
    return(x/compartment.initPop)

def simpleSaturation(x,compartment,compartment2,compartmentList):
    lamb = 0.2
    return(x/(1+lamb*compartment.typeList[1]))

def simpleSaturationDivPop(x,compartment,compartment2,compartmentList):
    lamb = 0.01
    return(x/((1+lamb*compartment.typeList[1])*compartment.getPopulation()))

def simpleTierDivPop(x,compartment,compartment2,compartmentList):
    infectious1 = compartment.typeList[1]
    infectious2 = compartment2.typeList[1]
    
    if infectious1 < 100:
        retVal = x
    else:
        retVal = x/50
        
    return(retVal/compartment.getPopulation())

def simpleTier(x,compartment,compartment2,compartmentList):
    infectious1 = compartment.typeList[1]
    infectious2 = compartment2.typeList[1]
    
    if infectious1 < 100 and infectious2 < 100:
        retVal = x
    else:
        retVal = x/50
        
    return(retVal)

def globalTierDivPop(x,compartment,compartment2,compartmentList):
    
    infectiousTotal = 0
    
    for comp in compartmentList:
        infectiousTotal = infectiousTotal + comp.typeList[1]
    
    if infectiousTotal < 150:
        retVal = x
    else:
        retVal = x/2
        
    return(retVal/compartment.getPopulation())

def globalTier(x,compartment,compartment2,compartmentList):
    
    infectiousTotal = 0
    
    for comp in compartmentList:
        infectiousTotal = infectiousTotal + comp.typeList[1]
    
    if infectiousTotal < 150:
        retVal = x
    else:
        retVal = x/2
        
    return(retVal)

def globalSaturation(x,compartment,compartment2,compartmentList):
    
    lamb = 1
    
    total = 0
    
    for compartment in compartmentList:
        total = total+compartment.typeList[1]
        
    return(x/(1+lamb*total))



#code for printing HKO trees in testing
def printTree2(rootNode):
    print(rootNode.partSum, end = '')
    print("")
    for child in rootNode.childeren:
        print (child.partSum, end = '')
        print("\t\t", end = '')

    print("")
    print("|", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            print(grandChild.partSum, end = '')
            print(" ", end = '')
        print("|", end = '')

def printTree3(rootNode):
    print(rootNode.partSum, end = '')
    print("")
    for child in rootNode.childeren:
        print (child.partSum, end = '')
        print(" ", end = '')

    print("")
    print("|", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            print(grandChild.partSum, end = '')
            print(" ", end = '')
        print("|", end = '')

    print("")
    print("||", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            for greatGrandChild in grandChild.childeren:
                print(greatGrandChild.partSum, end = '')
                print(" ", end = '')
            print("|", end = '')
        print("|", end = '')


def printTree4(rootNode):
    print(rootNode.partSum, end = '')
    print("")
    for child in rootNode.childeren:
        print (child.partSum, end = '')
        print(" ", end = '')

    print("")
    print("|", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            print(grandChild.partSum, end = '')
            print(" ", end = '')
        print("|", end = '')

    print("")
    print("||", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            for greatGrandChild in grandChild.childeren:
                print(greatGrandChild.partSum, end = '')
                print(" ", end = '')
            print("|", end = '')
        print("|", end = '')

    print("")
    print("|||", end = '')
    for child in rootNode.childeren:
        for grandChild in child.childeren:
            for greatGrandChild in grandChild.childeren:
                for greatGreatGrandChild in greatGrandChild.childeren:
                    print(greatGreatGrandChild.partSum, end = '')
                    print(" ", end = '')
                print("|", end = '')
            print("|", end = '')
        print("|", end = '')

    print("")
    
    
    
#Gillespie algorithm implementation
def gillespie(compartmentList,intraRuleList,interRuleList,finTime,maxIts):
    noCompartments = len(compartmentList)
    noTypes = compartmentList[0].noTypes
    time = 0
    data = np.zeros((maxIts+1,noTypes,noCompartments))
    timeData = np.zeros(maxIts+1)

    
    count = 0
    for compartment in compartmentList:
        data[0,:,count] = compartment.typeList
        count = count+1

    

    root = Node(0)
    root.addChild(Node(0))
    root.addChild(Node(0))

    for i in range (0,len(compartmentList)):
        root.childeren[0].addChild(Node(0))
        for j in range(0,len(intraRuleList)):
            root.childeren[0].childeren[i].addChild(Node(0))        
            intraRuleList[j].kineticConst = intraRuleList[j].kineticFunct(compartmentList[i].intraParams[j],compartmentList[i],compartmentList[i],compartmentList)
            root.childeren[0].childeren[i].childeren[j].partSum = intraRuleList[j].calculatePropensity(compartmentList[i])

    for i in range (0,len(compartmentList)):
        root.childeren[1].addChild(Node(0))

        for j in range(0,len(compartmentList)-1):
            root.childeren[1].childeren[i].addChild(Node(0))

            for k in range(0,len(interRuleList)):
                root.childeren[1].childeren[i].childeren[j].addChild(Node(0))
                #interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[k].interParams[i][k][j],compartmentList[j])
                interRuleList[k].kineticConst = interRuleList[k].kineticFunct(compartmentList[i].interParams[k][i][j],compartmentList[i],compartmentList[j],compartmentList)
                root.childeren[1].childeren[i].childeren[j].childeren[k].partSum = interRuleList[k].calculatePropensity(compartmentList[i])

    root.updatePartSum()

    iteration = 0
    
    printTree4(root)

    while time<finTime and  iteration<maxIts:

        iteration = iteration+1
       
        R0 = root.partSum

        r1 = np.random.uniform(0,1)
        #r1 = 0.2
        timeIncrement = -np.log(r1)/R0
        #timeIncrement = 0.69897000433/R0

        time = time+timeIncrement

        r2 = np.random.uniform(0,1)
        #r2 = 0.992
        

        if r2*R0>root.childeren[0].partSum:
            #inter
            ruleType = 1
            
            target = r2*R0 - root.childeren[0].partSum
            currentTotal = 0
            currentFromCompartment = 0
            fromCompartmentFound = False
            while not(fromCompartmentFound):
                if currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].partSum:
                    fromCompartmentFound = True
                else:
                    currentTotal = currentTotal+root.childeren[1].childeren[currentFromCompartment].partSum
                    currentFromCompartment = currentFromCompartment+1

            target = target - currentTotal
            currentTotal = 0
            currentToCompartment = 0
            toCompartmentFound = False
            while not(toCompartmentFound):
                if currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].partSum:
                    toCompartmentFound = True
                else:
                    currentTotal = currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].partSum
                    currentToCompartment = currentToCompartment+1


            target = target - currentTotal
            currentTotal = 0
            currentRule = 0
            ruleFound = False
            while not(ruleFound):
                if currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].childeren[currentRule].partSum:
                    ruleFound = True
                else:
                    currentTotal = currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].childeren[currentRule].partSum
                    currentRule = currentRule+1

            


        else:
            #intra
            ruleType = 0
            
            target = r2*R0
            currentTotal = 0
            currentCompartment = 0
            compartmentFound = False
            #print("target: ",target)
            while not(compartmentFound):
                if currentTotal<=target<=currentTotal+root.childeren[0].childeren[currentCompartment].partSum:
                    compartmentFound = True
                    #print("found current total: ",currentTotal)
                    #print("current rule: ",currentRule)
                else:
                    currentTotal = currentTotal+root.childeren[0].childeren[currentCompartment].partSum
                    currentCompartment = currentCompartment+1
                    #print("current total: ",currentTotal)
                    #print("current rule: ",currentRule)

            target = target - currentTotal
            #print("target: ",target)
            currentTotal = 0
            currentRule = 0
            ruleFound = False
            while not(ruleFound):
                if currentTotal<target<=currentTotal+root.childeren[0].childeren[currentCompartment].childeren[currentRule].partSum:
                    ruleFound = True
                else:
                    currentTotal = currentTotal+root.childeren[0].childeren[currentCompartment].childeren[currentRule].partSum
                    currentRule = currentRule+1
                    #print("current total: ",currentTotal)


        if ruleType==0:

            #execute rule
            
            intraRuleList[currentRule].executeRule(compartmentList[currentCompartment])
            
            selectedRule = intraRuleList[currentRule]
            
            oldSum2 = root.childeren[0].childeren[currentCompartment].partSum
            oldSum3 = root.childeren[0].partSum
            
            for i in range(0,len(intraRuleList)):
                #for j in range(0,len(intraRuleList[i].sourceComplex)):
                 #   if (intraRuleList[i].sourceComplex[j] > 0 and selectedRule.sourceComplex[j] > 0 ) or (intraRuleList[i].sourceComplex[j] > 0 and selectedRule.targetComplex[j] > 0):
                        
                oldSum1 = root.childeren[0].childeren[currentCompartment].childeren[i].partSum
                # oldSum2 = root.childeren[0].childeren[currentCompartment].partSum
                # oldSum3 = root.childeren[0].partSum
                
                intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentCompartment].intraParams[i],compartmentList[currentCompartment],compartmentList[currentCompartment],compartmentList)
                root.childeren[0].childeren[currentCompartment].childeren[i].partSum = intraRuleList[i].calculatePropensity(compartmentList[currentCompartment])
        
                root.childeren[0].childeren[currentCompartment].updatePartSumFromOneChild(i,oldSum1)
            root.childeren[0].updatePartSumFromOneChild(currentCompartment,oldSum2)
            root.updatePartSumFromOneChild(0,oldSum3)



            for i in range(0,len(interRuleList)):
                #for j in range(0,len(interRuleList[i].sourceComplex)):
                 #   if (interRuleList[i].sourceComplex[j] > 0 and selectedRule.sourceComplex[j] > 0 ) or (interRuleList[i].sourceComplex[j] > 0 and selectedRule.targetComplex[j] > 0):
                for k in range(0,noCompartments-1):
                    
                    oldSum1 = root.childeren[1].childeren[currentCompartment].childeren[k].childeren[i].partSum
                    oldSum2 = root.childeren[1].childeren[currentCompartment].childeren[k].partSum
                    oldSum3 = root.childeren[1].childeren[currentCompartment].partSum
                    oldSum4 = root.childeren[1].partSum
                    
                    #from currentCompartment to k
                    #interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentCompartment].interParams[i][currentCompartment][k],compartmentList[currentCompartment])
                    interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentCompartment].interParams[i][currentCompartment][k],compartmentList[currentCompartment],compartmentList[k],compartmentList)
                    root.childeren[1].childeren[currentCompartment].childeren[k].childeren[i].partSum = interRuleList[i].calculatePropensity(compartmentList[currentCompartment])
                    
                    root.childeren[1].childeren[currentCompartment].childeren[k].updatePartSumFromOneChild(i,oldSum1)
                    root.childeren[1].childeren[currentCompartment].updatePartSumFromOneChild(k,oldSum2)
                    root.childeren[1].updatePartSumFromOneChild(currentCompartment,oldSum3)
                    root.updatePartSumFromOneChild(1,oldSum4)
       
            
        else:
            
            #print("from ",currentFromCompartment, " to ",currentToCompartment)
            #print(compartmentList[currentFromCompartment].typeList,compartmentList[currentToCompartment].typeList)
            
            if currentFromCompartment <= currentToCompartment:
                interRuleList[currentRule].executeRule(compartmentList[currentFromCompartment],compartmentList[currentToCompartment+1])
            else:
                interRuleList[currentRule].executeRule(compartmentList[currentFromCompartment],compartmentList[currentToCompartment])
            #update
            
            #print(compartmentList[currentFromCompartment].typeList,compartmentList[currentToCompartment].typeList)
            selectedRule = interRuleList[currentRule]
            
            for i in range(0,len(intraRuleList)):
               # for j in range(0,len(intraRuleList[i].sourceComplex)):
                #    if (intraRuleList[i].sourceComplex[j] > 0 and selectedRule.sourceComplex[j] > 0 ):
                        
                        
                oldSum1 = root.childeren[0].childeren[currentFromCompartment].childeren[i].partSum
                oldSum2 = root.childeren[0].childeren[currentFromCompartment].partSum
                oldSum3 = root.childeren[0].partSum
                
                intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentFromCompartment].intraParams[i],compartmentList[currentFromCompartment],compartmentList[currentFromCompartment],compartmentList)
                root.childeren[0].childeren[currentFromCompartment].childeren[i].partSum = intraRuleList[i].calculatePropensity(compartmentList[currentFromCompartment])
        
                root.childeren[0].childeren[currentFromCompartment].updatePartSumFromOneChild(i,oldSum1)
                root.childeren[0].updatePartSumFromOneChild(currentFromCompartment,oldSum2)
                root.updatePartSumFromOneChild(0,oldSum3)
                
                        
                    
               #     if (intraRuleList[i].sourceComplex[j] > 0 and selectedRule.targetComplex[j] > 0):
                        
                oldSum1 = root.childeren[0].childeren[currentToCompartment].childeren[i].partSum
                oldSum2 = root.childeren[0].childeren[currentToCompartment].partSum
                oldSum3 = root.childeren[0].partSum
                
                intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentToCompartment].intraParams[i],compartmentList[currentToCompartment],compartmentList[currentToCompartment],compartmentList)
                root.childeren[0].childeren[currentToCompartment].childeren[i].partSum = intraRuleList[i].calculatePropensity(compartmentList[currentToCompartment])
        
                root.childeren[0].childeren[currentToCompartment].updatePartSumFromOneChild(i,oldSum1)
                root.childeren[0].updatePartSumFromOneChild(currentToCompartment,oldSum2)
                root.updatePartSumFromOneChild(0,oldSum3)
                
                

            for i in range(0,len(interRuleList)):
                #for j in range(0,len(interRuleList[i].sourceComplex)):
                 #   if (interRuleList[i].sourceComplex[j] > 0 and selectedRule.sourceComplex[j] > 0 ) :
                for k in range(0,noCompartments-1):
                    
                    oldSum1 = root.childeren[1].childeren[currentFromCompartment].childeren[k].childeren[i].partSum
                    oldSum2 = root.childeren[1].childeren[currentFromCompartment].childeren[k].partSum
                    oldSum3 = root.childeren[1].childeren[currentFromCompartment].partSum
                    oldSum4 = root.childeren[1].partSum
                    
                    #from currentCompartment to k
                    #interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentCompartment].interParams[i][currentCompartment][k],compartmentList[currentCompartment])
                    interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentFromCompartment].interParams[i][currentFromCompartment][k],compartmentList[currentFromCompartment],compartmentList[k],compartmentList)
                    root.childeren[1].childeren[currentFromCompartment].childeren[k].childeren[i].partSum = interRuleList[i].calculatePropensity(compartmentList[currentFromCompartment])
                    
                    root.childeren[1].childeren[currentFromCompartment].childeren[k].updatePartSumFromOneChild(i,oldSum1)
                    root.childeren[1].childeren[currentFromCompartment].updatePartSumFromOneChild(k,oldSum2)
                    root.childeren[1].updatePartSumFromOneChild(currentFromCompartment,oldSum3)
                    root.updatePartSumFromOneChild(1,oldSum4)
            
                    #if (interRuleList[i].sourceComplex[j] > 0 and selectedRule.targetComplex[j] > 0):
                for k in range(0,noCompartments-1):
                    
                    oldSum1 = root.childeren[1].childeren[currentToCompartment].childeren[k].childeren[i].partSum
                    oldSum2 = root.childeren[1].childeren[currentToCompartment].childeren[k].partSum
                    oldSum3 = root.childeren[1].childeren[currentToCompartment].partSum
                    oldSum4 = root.childeren[1].partSum
                    
                    #from currentCompartment to k
                    #interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentCompartment].interParams[i][currentCompartment][k],compartmentList[currentCompartment])
                    interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentToCompartment].interParams[i][currentToCompartment][k],compartmentList[currentToCompartment],compartmentList[k],compartmentList)
                    root.childeren[1].childeren[currentToCompartment].childeren[k].childeren[i].partSum = interRuleList[i].calculatePropensity(compartmentList[currentToCompartment])
                    
                    root.childeren[1].childeren[currentToCompartment].childeren[k].updatePartSumFromOneChild(i,oldSum1)
                    root.childeren[1].childeren[currentToCompartment].updatePartSumFromOneChild(k,oldSum2)
                    root.childeren[1].updatePartSumFromOneChild(currentToCompartment,oldSum3)
                    root.updatePartSumFromOneChild(1,oldSum4)
                    

        
        count = 0
        for compartment in compartmentList:
            data[iteration,:,count] = compartment.typeList
            count = count+1
        
        timeData[iteration] = time

    return(data,timeData,iteration)
        
        


#Code to implement a simple movement model with a complete adjacency graph with 3 compartments
noCompartments = 3

#SIRD types used. Rules are infection, recovery, death, loss of immunity. The last argument is the kinetic function
intraRuleListP = [intraRule([1,1,0,0],[0,2,0,0],constDivPop),intraRule([0,1,0,0],[0,0,1,0],const),intraRule([0,1,0,0],[0,0,0,1],const),intraRule([0,0,1,0],[1,0,0,0],const)]
#simple movement rules
interRuleListP = [interRule([1,0,0,0],[1,0,0,0],const),interRule([0,1,0,0],[0,1,0,0],const),interRule([0,0,1,0],[0,0,1,0],const)]

#transition matrix represents the rate of movement between compartments. Here we
#have a complete graph configuration
subSubMatrix = []
for i in range(0,noCompartments-1):
    subSubMatrix.append(2/500)
    
subMatrix = []
for i in range(0,noCompartments):
    subMatrix.append(subSubMatrix)
    
transitionMatrix = []
for i in range(0,len(interRuleListP)):
    transitionMatrix.append(subMatrix)
    
    
    
#for a chain, use the following instead
# subMatrix = []
# for i in range(0,noCompartments):
#     subSubMatrix = []
#     for j in range(0,noCompartments-1):
#         if i>j:
#             if j==i-1 or j==i:
#                 subSubMatrix.append(2/500)
#             else: 
#                 subSubMatrix.append(0)
#         else:
#             if j==i:
#                 subSubMatrix.append(2/500)
#             else:
#                 subSubMatrix.append(0)
                
    
#     subMatrix.append(subSubMatrix)
    
#compartmentListP stores the list of compartments used. The first parameter to compartment
#is the initial values for each type, the second is the parameters for the intracompartmental
#rules and the third the intercompartmental rules     
compartmentListP = []
compartmentListP.append(compartment([500-5,5,0,0],[0.5,0.07,0.02,0.005],transitionMatrix))
for i in range(1,noCompartments):
    compartmentListP.append(compartment([500,0,0,0],[0.5,0.07,0.02,0.005],transitionMatrix))


gillespieData = gillespie(compartmentListP, intraRuleListP, interRuleListP, 200,200000)

#The following code prints the output of the instance
noData = gillespieData[0]
timeDataUncut = gillespieData[1]
finIt = gillespieData[2]

timeData = timeDataUncut[:finIt]

comp1Sus = noData[:finIt,0,0]
comp2Sus = noData[:finIt,0,1]
comp3Sus = noData[:finIt,0,2]

comp1Inf = noData[:finIt,1,0]
comp2Inf = noData[:finIt,1,1]
comp3Inf = noData[:finIt,1,2]

comp1Rec = noData[:finIt,2,0]
comp2Rec = noData[:finIt,2,1]
comp3Rec = noData[:finIt,2,2]

comp1Dead = noData[:finIt,3,0]
comp2Dead = noData[:finIt,3,1]
comp3Dead = noData[:finIt,3,2]

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus, label="Susceptible")
line2,=ax.plot(timeData,comp1Inf, label="Infectious")
line3,=ax.plot(timeData,comp1Rec, label="Recovered")
line4,=ax.plot(timeData,comp1Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus, label="Susceptible")
line2,=ax.plot(timeData,comp2Inf, label="Infectious")
line3,=ax.plot(timeData,comp2Rec, label="Recovered")
line4,=ax.plot(timeData,comp2Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()



fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus, label="Susceptible")
line2,=ax.plot(timeData,comp3Inf, label="Infectious")
line3,=ax.plot(timeData,comp3Rec, label="Recovered")
line4,=ax.plot(timeData,comp3Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()

    

#Code to implement a visitation model with a complete adjacency graph with 3 compartments
noCompartments = 3
compartmentList = []
intraRuleList = []

#intracompartmental rules must be constructed more carefully now

#infection
sourceTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        sourceTypes.append(0)
        
targetTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        targetTypes.append(0)


sourceTypes[0] = 1
sourceTypes[1] = 1
targetTypes[1] = 2

intraRuleList.append(intraRule(sourceTypes,targetTypes,constDivPop))  


#recovery
sourceTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        sourceTypes.append(0)
        
targetTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        targetTypes.append(0)


sourceTypes[1] = 1
targetTypes[2] = 1

intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  

#death

sourceTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        sourceTypes.append(0)
        
targetTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        targetTypes.append(0)


sourceTypes[1] = 1
targetTypes[3] = 1

intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  

#loss of immunity

sourceTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        sourceTypes.append(0)
        
targetTypes = [0,0,0,0]
for l in range(1,noCompartments):
    for m in range(0,3):
        targetTypes.append(0)


sourceTypes[2] = 1
targetTypes[0] = 1

intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  


for i in range(0,noCompartments-1):

    #infecting visitor
    sourceTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            targetTypes.append(0)


    sourceTypes[1] = 1
    sourceTypes[0+4+3*i] = 1
    targetTypes[1] = 1
    targetTypes[1+4+3*i] = 1


    intraRuleList.append(intraRule(sourceTypes,targetTypes,constDivPop))  

    
    
    #infection from visitor
    sourceTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            targetTypes.append(0)


    sourceTypes[0] = 1
    sourceTypes[1+4+3*i] = 1
    targetTypes[1] = 1
    targetTypes[1+4+3*i] = 1

    intraRuleList.append(intraRule(sourceTypes,targetTypes,constDivPop))  

    
    #recovery of visitor
    
    sourceTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            targetTypes.append(0)


    sourceTypes[1+4+3*i] = 1
    targetTypes[2+4+3*i] = 1
    
    intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  

    #death of visitor

    sourceTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            targetTypes.append(0)


    sourceTypes[1+4+3*i] = 1
    targetTypes[3] = 1
    
    intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  

    #loss of immunity of visitor

    sourceTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for l in range(1,noCompartments):
        for m in range(0,3):
            targetTypes.append(0)


    sourceTypes[2+4+3*i] = 1
    targetTypes[0+4+3*i] = 1
    
    intraRuleList.append(intraRule(sourceTypes,targetTypes,const))  

    
    



for j in range(0,noCompartments-1):
    for k in range(0,noCompartments-1):
        
        #infection between two visitors
        
        sourceTypes = [0,0,0,0]
        for l in range(1,noCompartments):
            for m in range(0,3):
                sourceTypes.append(0)
                
        targetTypes = [0,0,0,0]
        for l in range(1,noCompartments):
            for m in range(0,3):
                targetTypes.append(0)
    
    
        sourceTypes[1+4+3*j] = 1
        sourceTypes[0+4+3*k] = 1
        targetTypes[1+4+3*j] = 1
        targetTypes[1+4+3*k] = targetTypes[1+4+3*k] + 1

        
        intraRuleList.append(intraRule(sourceTypes,targetTypes,constDivPop))  
    

            

#movement rules for visitors both to and home from all other compartments
interRuleList = []

for j in range(0,noCompartments-1):
    
    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[0] = 1
    targetTypes[4+3*j] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))
    
    
    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[4+3*j] = 1
    targetTypes[0] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))

    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[1] = 1
    targetTypes[1+4+3*j] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))

    
    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[1+4+3*j] = 1
    targetTypes[1] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))

    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[2] = 1
    targetTypes[2+4+3*j] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))

    
    
    sourceTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            sourceTypes.append(0)
            
    targetTypes = [0,0,0,0]
    for k in range(1,noCompartments):
        for l in range(0,3):
            targetTypes.append(0)
     
    sourceTypes[2+4+3*j] = 1
    targetTypes[2] = 1
    
    interRuleList.append(interRule(sourceTypes,targetTypes,const))

    
    
    
  
interParams = []

#set parameters for complete adjacency graph
for j in range (0,(noCompartments-1)):
    for i in range (0,3):
        theseParams = []
        
        for k in range(0,noCompartments):
            theseSubParams = []
            for l in range(0,noCompartments-1):
                
                if k>l:
                    target = k-1
                    
                else:
                    target = k
                    
                if target==j:
                    
                    if i==1:
                        theseSubParams.append(1/500)
                    else:
                        theseSubParams.append(1/500)               
                    
                else:
                    theseSubParams.append(0)
                    
            
                    
            theseParams.append(theseSubParams)
        
            
        interParams.append(theseParams)
        

        theseParams = []
        
        for k in range(0,noCompartments):
            
            
            
            theseSubParams = []
            for l in range(0,noCompartments-1):
                
                if k>l:
                    target = l
                else:
                    target = l
                    
                
                    
                if target==j:
                    
                    
                    theseSubParams.append(1)                
                    
                else:
                    theseSubParams.append(0)
                    
            
                    
            theseParams.append(theseSubParams)
        
            
        interParams.append(theseParams)
        

#For a chain, use the following instead

#interParams = []

# for i in range (0,3):
#     for j in range (0,(noCompartments-1)):
#         theseParams = []
        
#         for k in range(0,noCompartments):
#             theseSubParams = []
#             for l in range(0,noCompartments-1):
                
#                 if k>l:
#                     target = k-1
#                 else:
#                     target = k
                    
#                 if target==j:
                    
#                     
#                     if k>l:
#                         if l==k-1 or l==k:
#                             theseSubParams.append(1/500)
#                         else:
#                             theseSubParams.append(0)
                    
#                     else:
#                         if l==k :
#                             theseSubParams.append(1/500)
#                         else:
#                             theseSubParams.append(0)                    
                    
#                 else:
#                     theseSubParams.append(0)
                    
            
                    
#             theseParams.append(theseSubParams)
        
            
#         interParams.append(theseParams)
        

#         theseParams = []

#         for k in range(0,noCompartments):



#             theseSubParams = []
#             for l in range(0,noCompartments-1):

#                 if k>l:
#                     target = l
#                 else:
#                     target = l



#                 if target==j:


#                     theseSubParams.append(1)                

#                 else:
#                     theseSubParams.append(0)



#             theseParams.append(theseSubParams)


#         interParams.append(theseParams)



#set parameters for intracompartmental rules in the order the rules are defined
intraParams = [0.5,0.07,0.02,0.005]

for i in range(0,noCompartments-1):
    intraParams.append(0.5)
    intraParams.append(0.5)
    intraParams.append(0.07)
    intraParams.append(0.02)
    intraParams.append(0.005)
    
for j in range(0,noCompartments-1):
    for k in range(0,noCompartments-1):
        intraParams.append(0.5)



comp1Types = [500-15,5,0,0,5,0,0,5,0,0]
compartmentList = []
compartmentList.append(compartment(comp1Types,intraParams,interParams))


for i in range(0,noCompartments-1):
    compartmentList.append(compartment([500-10,0,0,0,5,0,0,5,0,0],intraParams,interParams))

    
gillespieData = gillespie(compartmentList, intraRuleList, interRuleList, 200,2000000)
    
    

noData = gillespieData[0]
timeDataUncut = gillespieData[1]
finIt = gillespieData[2]

timeData = timeDataUncut[:finIt]

comp1Sus = noData[:finIt,0,0]
comp2Sus = noData[:finIt,0,1]
comp3Sus = noData[:finIt,0,2]

comp1Inf = noData[:finIt,1,0]
comp2Inf = noData[:finIt,1,1]
comp3Inf = noData[:finIt,1,2]

comp1Rec = noData[:finIt,2,0]
comp2Rec = noData[:finIt,2,1]
comp3Rec = noData[:finIt,2,2]

comp1Dead = noData[:finIt,3,0]
comp2Dead = noData[:finIt,3,1]
comp3Dead = noData[:finIt,3,2]

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus, label="Susceptible")
line2,=ax.plot(timeData,comp1Inf, label="Infectious")
line3,=ax.plot(timeData,comp1Rec, label="Recovered")
line4,=ax.plot(timeData,comp1Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus, label="Susceptible")
line2,=ax.plot(timeData,comp2Inf, label="Infectious")
line3,=ax.plot(timeData,comp2Rec, label="Recovered")
line4,=ax.plot(timeData,comp2Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()



fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus, label="Susceptible")
line2,=ax.plot(timeData,comp3Inf, label="Infectious")
line3,=ax.plot(timeData,comp3Rec, label="Recovered")
line4,=ax.plot(timeData,comp3Dead, label="Dead")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()




