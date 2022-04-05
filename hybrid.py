#This file contains the neccecary code to run simulations for the
#hybrid model that I demonstrate in the applications to Covid-19 section

#import neccecary libraries
import numpy as np
import matplotlib.pyplot as plt
import time

#define functions for later use
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

#define node for HKO tree
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

    
    #this will work but it not as efficiant as possible for updates after rules
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

#define rules
class intraRule:
    #seperateing kineticCOnst and kineticFunct may not be neccecary for computational
    #efficiancy
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
    #seperateing kineticConst and kineticFunct may not be neccecary for computational
    #efficiancy
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
    
    

#define compartments
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
        




#define kinetic functions
def const(x,compartment,compartmentList):
    return(x)

def constDivPop(x,compartment,compartmentList):
    return(x/compartment.initPop)

def simpleSaturation(x,compartment,compartmentList):
    lamb = 1
    return(x/(1+lamb*compartment.typeList[1]))



def simpleSaturationDivPop(x,compartment,compartmentList):
    lamb = 0.01
    return(x/((1+lamb*compartment.typeList[1])*compartment.getPopulation()))

def simpleTier(x,compartment,compartmentList):
    infectious = compartment.typeList[1]
    
    if infectious < 100:
        retVal = x
    else:
        retVal = x/2
        
    return(retVal/compartment.getPopulation())

def globalTier(x,compartment,compartmentList):
    
    infectiousTotal = 0
    
    for comp in compartmentList:
        infectiousTotal = infectiousTotal + comp.typeList[1]
    
    if infectiousTotal < 150:
        retVal = x
    else:
        retVal = x/2
        
    return(retVal/compartment.getPopulation())

def globalSaturation(x,compartment,compartmentList):
    
    lamb = 1
    
    total = 0
    
    for compartment in compartmentList:
        total = total+compartment.typeList[1]
        
    return(x/(1+lamb*total))




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

#main Gillespie algorithm
def gillespie(compartmentList,intraRuleList,interRuleList,finTime,maxIts):
    #np.random.seed(9)
    noCompartments = len(compartmentList)
    noTypes = compartmentList[0].noTypes
    time = 0
    data = np.zeros((maxIts+1,noTypes,noCompartments))
    timeData = np.zeros(maxIts+1)

    
    count = 0
    for compartment in compartmentList:
        print(count)
        print(compartment.typeList)
        data[0,:,count] = compartment.typeList
        count = count+1

    

    root = Node(0)
    root.addChild(Node(0))
    root.addChild(Node(0))

    for i in range (0,len(compartmentList)):
        root.childeren[0].addChild(Node(0))
        for j in range(0,len(intraRuleList)):
            root.childeren[0].childeren[i].addChild(Node(0))        
            intraRuleList[j].kineticConst = intraRuleList[j].kineticFunct(compartmentList[i].intraParams[j],compartmentList[i],compartmentList)
            root.childeren[0].childeren[i].childeren[j].partSum = intraRuleList[j].calculatePropensity(compartmentList[i])

    for i in range (0,len(compartmentList)):
        root.childeren[1].addChild(Node(0))

        for j in range(0,len(compartmentList)-1):
            root.childeren[1].childeren[i].addChild(Node(0))

            for k in range(0,len(interRuleList)):
                root.childeren[1].childeren[i].childeren[j].addChild(Node(0))
                #interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[k].interParams[i][k][j],compartmentList[j])
                interRuleList[k].kineticConst = interRuleList[k].kineticFunct(compartmentList[i].interParams[k][i][j],compartmentList[i],compartmentList)
                root.childeren[1].childeren[i].childeren[j].childeren[k].partSum = interRuleList[k].calculatePropensity(compartmentList[i])

    root.updatePartSum()

    iteration = 0
    
    #printTree4(root)

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
        
        executeRule = True
        

        if r2*R0>root.childeren[0].partSum:
            #inter
            ruleType = 1
            
            target = r2*R0 - root.childeren[0].partSum
            currentTotal = 0
            currentFromCompartment = 0
            fromCompartmentFound = False
            while not(fromCompartmentFound):
                if currentFromCompartment == noCompartments:
                    fromCompartmentFound = True
                    currentFromCompartment = currentFromCompartment-1
                    executeRule = False
                elif currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].partSum:
                    fromCompartmentFound = True
                else:
                    currentTotal = currentTotal+root.childeren[1].childeren[currentFromCompartment].partSum
                    currentFromCompartment = currentFromCompartment+1

            target = target - currentTotal
            currentTotal = 0
            currentToCompartment = 0
            toCompartmentFound = False
            while not(toCompartmentFound):
                if currentToCompartment == noCompartments-1:
                    toCompartmentFound = True
                    currentToCompartment = currentToCompartment-1
                    executeRule = False
                elif currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].partSum:
                    toCompartmentFound = True
                else:
                    currentTotal = currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].partSum
                    currentToCompartment = currentToCompartment+1


            target = target - currentTotal
            currentTotal = 0
            currentRule = 0
            ruleFound = False
            while not(ruleFound):
                if currentRule == len(interRuleList):
                    ruleFound = True
                    currentRule = currentRule-1
                    executeRule = False
                elif currentTotal<target<=currentTotal+root.childeren[1].childeren[currentFromCompartment].childeren[currentToCompartment].childeren[currentRule].partSum:
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
                if currentCompartment == noCompartments:
                    compartmentFound = True
                    currentCompartment = currentCompartment-1
                    executeRule = False
                elif currentTotal<=target<=currentTotal+root.childeren[0].childeren[currentCompartment].partSum:
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
                if currentRule == len(intraRuleList):
                    ruleFound = True
                    currentRule = currentRule-1
                    executeRule = False
                elif currentTotal<target<=currentTotal+root.childeren[0].childeren[currentCompartment].childeren[currentRule].partSum:
                    ruleFound = True
                else:
                    currentTotal = currentTotal+root.childeren[0].childeren[currentCompartment].childeren[currentRule].partSum
                    currentRule = currentRule+1
                    #print("current total: ",currentTotal)


        if executeRule:
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

                    intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentCompartment].intraParams[i],compartmentList[currentCompartment],compartmentList)
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
                        interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentCompartment].interParams[i][currentCompartment][k],compartmentList[k],compartmentList)
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

                    intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentFromCompartment].intraParams[i],compartmentList[currentFromCompartment],compartmentList)
                    root.childeren[0].childeren[currentFromCompartment].childeren[i].partSum = intraRuleList[i].calculatePropensity(compartmentList[currentFromCompartment])

                    root.childeren[0].childeren[currentFromCompartment].updatePartSumFromOneChild(i,oldSum1)
                    root.childeren[0].updatePartSumFromOneChild(currentFromCompartment,oldSum2)
                    root.updatePartSumFromOneChild(0,oldSum3)



                   #     if (intraRuleList[i].sourceComplex[j] > 0 and selectedRule.targetComplex[j] > 0):

                    oldSum1 = root.childeren[0].childeren[currentToCompartment].childeren[i].partSum
                    oldSum2 = root.childeren[0].childeren[currentToCompartment].partSum
                    oldSum3 = root.childeren[0].partSum

                    intraRuleList[i].kineticConst = intraRuleList[i].kineticFunct(compartmentList[currentToCompartment].intraParams[i],compartmentList[currentToCompartment],compartmentList)
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
                        interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentFromCompartment].interParams[i][currentFromCompartment][k],compartmentList[k],compartmentList)
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
                        interRuleList[i].kineticConst = interRuleList[i].kineticFunct(compartmentList[currentToCompartment].interParams[i][currentToCompartment][k],compartmentList[k],compartmentList)
                        root.childeren[1].childeren[currentToCompartment].childeren[k].childeren[i].partSum = interRuleList[i].calculatePropensity(compartmentList[currentToCompartment])

                        root.childeren[1].childeren[currentToCompartment].childeren[k].updatePartSumFromOneChild(i,oldSum1)
                        root.childeren[1].childeren[currentToCompartment].updatePartSumFromOneChild(k,oldSum2)
                        root.childeren[1].updatePartSumFromOneChild(currentToCompartment,oldSum3)
                        root.updatePartSumFromOneChild(1,oldSum4)

        else:
            time = time-timeIncrement
            #print(ruleType,time)

        
        count = 0
        for compartment in compartmentList:
            data[iteration,:,count] = compartment.typeList
            count = count+1
        
        timeData[iteration] = time

    return(data,timeData,iteration)


#hybrid intracompartmental rules for simple movement

intraRuleList = []

thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[3] = 1
thisTarget[3] = 2


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[3] = 1
thisTarget[3] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[4] = 1
thisTarget[3] = 1
thisTarget[4] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[4] = 1
thisTarget[4] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[5] = 1
thisTarget[3] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[5] = 1
thisTarget[5] = 2


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[6] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[4] = 1
thisTarget[7] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[8] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[9] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[4] = 1
thisTarget[10] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[11] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisTarget[1] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))


thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[4] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[6] = 1
thisTarget[7] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))



thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisTarget[0] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[3] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[8] = 1
thisTarget[6] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))






#================================================================
#hybrid intercompartmental rules for simple movement

interRuleList = []

for i in range(0,9):
    
    thisSource= []
    thisTarget = []
    for j in range(0,12):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[i] = 1
    thisTarget[i] = 1
    
    print(thisSource)
    print(thisTarget)
    print("")
    
    interRuleList.append(interRule(thisSource,thisTarget,const))



print("\n\n\n")

#interCompartmental parameters for simple movement

noCompartments = 3


subSubMatrix = []
for i in range(0,noCompartments-1):
    subSubMatrix.append(2/500)
    
subSubMatrixZero = []
for i in range(0,noCompartments-1):
    subSubMatrixZero.append(0/500)
    
subMatrix = []
for i in range(0,noCompartments):
    subMatrix.append(subSubMatrix)
    
subMatrixZero = []
for i in range(0,noCompartments):
    subMatrixZero.append(subSubMatrixZero)
    
    
transitionMatrix = []
for i in range(0,len(interRuleList)):
    if i==4 or i==8 or i==0 or i==3 or i==6:
        transitionMatrix.append(subMatrix)
    else:
        transitionMatrix.append(subMatrix)
    
    
    
    
#create compartments and run algorithm
    
compartmentList = []
compartmentTypes = [500-5,0,0,5,0,0,0,0,0,0,0,0]

compartmentList.append(compartment(compartmentTypes,[0.5,0.5,0.5,0.5,0.5,0.5,0.07,0.07,0.07,0.02,0.02,0.02,500,500,500,0.09,0.09,0.09],transitionMatrix))


for i in range(1,noCompartments):
    compartmentTypes = [500,0,0,0,0,0,0,0,0,0,0,0]
    compartmentList.append(compartment(compartmentTypes,[0.5,0.5,0.5,0.5,0.5,0.5,0.07,0.07,0.07,0.02,0.02,0.02,500,500,500,0.09,0.09,0.09],transitionMatrix))


gillespieData = gillespie(compartmentList, intraRuleList, interRuleList, 200,2000000)


#display output of instance

noData = gillespieData[0]
timeDataUncut = gillespieData[1]
finIt = gillespieData[2]

timeData = timeDataUncut[:finIt]

comp1Sus0 = noData[:finIt,0,0]
comp2Sus0 = noData[:finIt,0,1]
comp3Sus0 = noData[:finIt,0,2]
comp1Sus1 = noData[:finIt,1,0]
comp2Sus1 = noData[:finIt,1,1]
comp3Sus1 = noData[:finIt,1,2]
comp1Sus2 = noData[:finIt,2,0]
comp2Sus2 = noData[:finIt,2,1]
comp3Sus2 = noData[:finIt,2,2]

comp1Inf0 = noData[:finIt,3,0]
comp2Inf0 = noData[:finIt,3,1]
comp3Inf0 = noData[:finIt,3,2]
comp1Inf1 = noData[:finIt,4,0]
comp2Inf1 = noData[:finIt,4,1]
comp3Inf1 = noData[:finIt,4,2]
comp1Inf2 = noData[:finIt,5,0]
comp2Inf2 = noData[:finIt,5,1]
comp3Inf2 = noData[:finIt,5,2]

comp1Rec0 = noData[:finIt,6,0]
comp2Rec0 = noData[:finIt,6,1]
comp3Rec0 = noData[:finIt,6,2]
comp1Rec1 = noData[:finIt,7,0]
comp2Rec1 = noData[:finIt,7,1]
comp3Rec1 = noData[:finIt,7,2]
comp1Rec2 = noData[:finIt,8,0]
comp2Rec2 = noData[:finIt,8,1]
comp3Rec2 = noData[:finIt,8,2]

comp1Dead0 = noData[:finIt,9,0]
comp2Dead0 = noData[:finIt,9,1]
comp3Dead0 = noData[:finIt,9,2]
comp1Dead1 = noData[:finIt,10,0]
comp2Dead1 = noData[:finIt,10,1]
comp3Dead1 = noData[:finIt,10,2]
comp1Dead2 = noData[:finIt,11,0]
comp2Dead2 = noData[:finIt,11,1]
comp3Dead2 = noData[:finIt,11,2]

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp1Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp1Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp1Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp1Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp1Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp1Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp1Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp1Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp1Dead0, label="Dead0")
line4,=ax.plot(timeData,comp1Dead1, label="Dead1")
line4,=ax.plot(timeData,comp1Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus0+comp1Sus1+comp1Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Inf0+comp1Inf1+comp1Inf2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Rec0+comp1Rec1+comp1Rec2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Dead0+comp1Dead1+comp1Dead2, label="Susceptible total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp2Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp2Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp2Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp2Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp2Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp2Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp2Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp2Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp2Dead0, label="Dead0")
line4,=ax.plot(timeData,comp2Dead1, label="Dead1")
line4,=ax.plot(timeData,comp2Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus0+comp2Sus1+comp2Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp2Inf0+comp2Inf1+comp2Inf2, label="Infectious total")
line1,=ax.plot(timeData,comp2Rec0+comp2Rec1+comp2Rec2, label="Recovered total")
line1,=ax.plot(timeData,comp2Dead0+comp2Dead1+comp2Dead2, label="Dead total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()



fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp3Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp3Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp3Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp3Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp3Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp3Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp3Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp3Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp3Dead0, label="Dead0")
line4,=ax.plot(timeData,comp3Dead1, label="Dead1")
line4,=ax.plot(timeData,comp3Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus0+comp3Sus1+comp3Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp3Inf0+comp3Inf1+comp3Inf2, label="Infectious total")
line1,=ax.plot(timeData,comp3Rec0+comp3Rec1+comp3Rec2, label="Recovered total")
line1,=ax.plot(timeData,comp3Dead0+comp3Dead1+comp3Dead2, label="Dead total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 simple movement')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()





#============================================================

#visitation

noCompartments = 3

#hybrid intracompartmental rules for visitation

intraRuleList = []


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[3] = 1
thisTarget[3] = 2

print(thisSource)
print(thisTarget)

intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[3] = 1
thisTarget[3] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[4] = 1
thisTarget[3] = 1
thisTarget[4] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[4] = 1
thisTarget[4] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisSource[5] = 1
thisTarget[3] = 1
thisTarget[5] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))





thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisSource[5] = 1
thisTarget[5] = 2


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))




thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[6] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[4] = 1
thisTarget[7] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[8] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[9] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[4] = 1
thisTarget[10] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[11] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[0] = 1
thisTarget[1] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[3] = 1
thisTarget[4] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[6] = 1
thisTarget[7] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))



thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[1] = 1
thisTarget[0] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[5] = 1
thisTarget[3] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))


thisSource= []
thisTarget = []
for i in range(0,12+9*(noCompartments-1)):
    thisSource.append(0)
    thisTarget.append(0)
    
thisSource[8] = 1
thisTarget[6] = 1


intraRuleList.append(intraRule(thisSource,thisTarget,const))






for i in range(0,noCompartments-1):
    
    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
        
    thisSource[0] = 1
    thisSource[12+9*i+3] = 1
    thisTarget[3] = 1
    thisTarget[12+9*i+3] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    


    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[1] = 1
    thisSource[12+9*i+3] = 1
    thisTarget[5] = 1
    thisTarget[12+9*i+3] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[0] = 1
    thisSource[12+9*i+4] = 1
    thisTarget[3] = 1
    thisTarget[12+9*i+4] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[1] = 1
    thisSource[12+9*i+4] = 1
    thisTarget[5] = 1
    thisTarget[12+9*i+4] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[0] = 1
    thisSource[12+9*i+5] = 1
    thisTarget[3] = 1
    thisTarget[12+9*i+5] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[1] = 1
    thisSource[12+9*i+5] = 1
    thisTarget[5] = 1
    thisTarget[12+9*i+5] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+0] = 1
    thisSource[3] = 1
    thisTarget[12+9*i+3] = 1
    thisTarget[3] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+1] = 1
    thisSource[3] = 1
    thisTarget[12+9*i+5] = 1
    thisTarget[3] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    


    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+0] = 1
    thisSource[4] = 1
    thisTarget[12+9*i+3] = 1
    thisTarget[4] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+1] = 1
    thisSource[4] = 1
    thisTarget[12+9*i+5] = 1
    thisTarget[4] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+0] = 1
    thisSource[5] = 1
    thisTarget[12+9*i+3] = 1
    thisTarget[5] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+1] = 1
    thisSource[5] = 1
    thisTarget[12+9*i+5] = 1
    thisTarget[5] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    


    for j in range(0,noCompartments-1):
        
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+0] = 1
        thisSource[12+9*j+3] = 1
        thisTarget[12+9*i+3] = thisTarget[12+9*i+3]+1
        thisTarget[12+9*j+3] = thisTarget[12+9*j+3]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+1] = 1
        thisSource[12+9*j+3] = 1
        thisTarget[12+9*i+5] = thisTarget[12+9*i+5]+1
        thisTarget[12+9*j+3] = thisTarget[12+9*j+3]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
    
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+0] = 1
        thisSource[12+9*j+4] = 1
        thisTarget[12+9*i+3] = thisTarget[12+9*i+3]+1
        thisTarget[12+9*j+4] = thisTarget[12+9*j+4]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+1] = 1
        thisSource[12+9*j+4] = 1
        thisTarget[12+9*i+5] = thisTarget[12+9*i+5]+1
        thisTarget[12+9*j+4] = thisTarget[12+9*j+4]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+0] = 1
        thisSource[12+9*j+5] = 1
        thisTarget[12+9*i+3] = thisTarget[12+9*i+3]+1
        thisTarget[12+9*j+5] = thisTarget[12+9*j+5]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
    
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[12+9*i+1] = 1
        thisSource[12+9*j+5] = 1
        thisTarget[12+9*i+5] = thisTarget[12+9*i+5]+1
        thisTarget[12+9*j+5] = thisTarget[12+9*j+5]+1
        
        
        intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
        
          

    
    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+3] = 1
    thisTarget[12+9*i+6] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    


    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+4] = 1
    thisTarget[12+9*i+7] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    



    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+5] = 1
    thisTarget[12+9*i+8] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    


    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+3] = 1
    thisTarget[9] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    


    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+4] = 1
    thisTarget[10] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    



    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+5] = 1
    thisTarget[11] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))

    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+0] = 1
    thisTarget[12+9*i+1] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+3] = 1
    thisTarget[12+9*i+4] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+6] = 1
    thisTarget[12+9*i+7] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,constDivPop))
    

    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+1] = 1
    thisTarget[12+9*i+0] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+5] = 1
    thisTarget[12+9*i+3] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    
    thisSource= []
    thisTarget = []
    for j in range(0,12+9*(noCompartments-1)):
        thisSource.append(0)
        thisTarget.append(0)
        
    thisSource[12+9*i+8] = 1
    thisTarget[12+9*i+6] = 1
    
    
    intraRuleList.append(intraRule(thisSource,thisTarget,const))
    



#================================================================
#hybrid intercompartmental rules for visitation

interRuleList = []

for i in range(0,9):
    
    for j in range(0,noCompartments-1):
        
        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[i] = 1
        thisTarget[i+12+9*j] = 1
        
        print(thisSource)
        print(thisTarget)
        print("")
        
        interRuleList.append(interRule(thisSource,thisTarget,const))
    

        thisSource= []
        thisTarget = []
        for k in range(0,12+9*(noCompartments-1)):
            thisSource.append(0)
            thisTarget.append(0)
            
        thisSource[i+12+9*j] = 1
        thisTarget[i] = 1
        
        print(thisSource)
        print(thisTarget)
        print("")
        
        interRuleList.append(interRule(thisSource,thisTarget,const))
    


#============================================================

#hybrid intercompartmental parameters for visitation
  
interParams = []


for j in range (0,(noCompartments-1)):
    for i in range (0,9):
        theseParams = []
        
        for k in range(0,noCompartments):
            theseSubParams = []
            for l in range(0,noCompartments-1):
                
                if k>l:
                    target = k-1
 
                else:
                    target = k
                    

                if target==j:
                    
                    if i==4 or i==8 or i==0 or i==3 or i==6:
                        theseSubParams.append(0/500)
                    else:
                        theseSubParams.append(1/500)               
                    
                else:
                    theseSubParams.append(0)
                    
            
                    
            theseParams.append(theseSubParams)
        
            
        interParams.append(theseParams)
        print(theseParams)

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
  

#hybrid intracompartmental rules for visitation
#intraParams = [0.5,0.5,0,0,0,0,0.07,0.07,0.07,0.02,0.02,0.02,50,50,50,0.09,0.09,0.09]
intraParams = [0.5,0.5,0.5,0.5,0.5,0.5,0.07,0.07,0.07,0.02,0.02,0.02,500,500,500,0.09,0.09,0.09]

for i in range(0,noCompartments-1):
    
    intraParams.append(0.5)
    intraParams.append(0.5)
    intraParams.append(0.5)
    intraParams.append(0.5)
    intraParams.append(0.5)
    intraParams.append(0.5)
    
    intraParams.append(0.5)
    intraParams.append(0.0)
    intraParams.append(0.5)
    intraParams.append(0.0)
    intraParams.append(0.5)
    intraParams.append(0.0)
    
    for j in range(0,noCompartments-1):
        intraParams.append(0.5)
        intraParams.append(0.0)
        intraParams.append(0.5)
        intraParams.append(0.0)
        intraParams.append(0.5)
        intraParams.append(0.0)
        
    intraParams.append(0.07)
    intraParams.append(0.07)
    intraParams.append(0.07)
    
    intraParams.append(0.02)
    intraParams.append(0.02)
    intraParams.append(0.02)
    
    intraParams.append(50)
    intraParams.append(50)
    intraParams.append(50)
    
    intraParams.append(0.09)
    intraParams.append(0.09)
    intraParams.append(0.09)
    
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
    
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
    
#     for j in range(0,noCompartments-1):
#         intraParams.append(0)
#         intraParams.append(0)
#         intraParams.append(0)
#         intraParams.append(0)
#         intraParams.append(0)
#         intraParams.append(0)
        
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
    
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
    
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
    
#     intraParams.append(0)
#     intraParams.append(0)
#     intraParams.append(0)
  
    
    
print(intraParams)

compartmentList = []

compartmentTypes = [500-5,0,0,5,0,0,0,0,0,0,0,0]
for i in range(0,(noCompartments-1)*9):
    compartmentTypes.append(0)

compartmentList.append(compartment(compartmentTypes,intraParams,interParams))

compartmentTypes = [500,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,(noCompartments-1)*9):
    compartmentTypes.append(0)

compartmentList.append(compartment(compartmentTypes,intraParams,interParams))

compartmentTypes = [499,1,0,0,0,0,0,0,0,0,0,0]
for i in range(0,(noCompartments-1)*9):
    compartmentTypes.append(0)
compartmentList.append(compartment(compartmentTypes,intraParams,interParams))

startTime = time.time()
gillespieData = gillespie(compartmentList, intraRuleList, interRuleList, 200,2000000)
endTime = time.time()
print(endTime-startTime)


noData = gillespieData[0]
timeDataUncut = gillespieData[1]
finIt = gillespieData[2]

timeData = timeDataUncut[:finIt]

comp1Sus0 = noData[:finIt,0,0]
comp2Sus0 = noData[:finIt,0,1]
comp3Sus0 = noData[:finIt,0,2]
comp1Sus1 = noData[:finIt,1,0]
comp2Sus1 = noData[:finIt,1,1]
comp3Sus1 = noData[:finIt,1,2]
comp1Sus2 = noData[:finIt,2,0]
comp2Sus2 = noData[:finIt,2,1]
comp3Sus2 = noData[:finIt,2,2]

comp1Sus01 = noData[:finIt,0+12,0]
comp1Sus11 = noData[:finIt,1+12,0]
comp1Sus21 = noData[:finIt,2+12,0]
comp1Sus02 = noData[:finIt,0+12+9,0]
comp1Sus12 = noData[:finIt,1+12+9,0]
comp1Sus22 = noData[:finIt,2+12+9,0]
comp1Inf01 = noData[:finIt,0+12+3,0]
comp1Inf11 = noData[:finIt,1+12+3,0]
comp1Inf21 = noData[:finIt,2+12+3,0]
comp1Inf02 = noData[:finIt,0+12+9+3,0]
comp1Inf12 = noData[:finIt,1+12+9+3,0]
comp1Inf22 = noData[:finIt,2+12+9+3,0]
comp1Rec01 = noData[:finIt,0+12+6,0]
comp1Rec11 = noData[:finIt,1+12+6,0]
comp1Rec21 = noData[:finIt,2+12+6,0]
comp1Rec02 = noData[:finIt,0+12+9+6,0]
comp1Rec12 = noData[:finIt,1+12+9+6,0]
comp1Rec22 = noData[:finIt,2+12+9+6,0]

comp1Inf0 = noData[:finIt,3,0]
comp2Inf0 = noData[:finIt,3,1]
comp3Inf0 = noData[:finIt,3,2]
comp1Inf1 = noData[:finIt,4,0]
comp2Inf1 = noData[:finIt,4,1]
comp3Inf1 = noData[:finIt,4,2]
comp1Inf2 = noData[:finIt,5,0]
comp2Inf2 = noData[:finIt,5,1]
comp3Inf2 = noData[:finIt,5,2]

comp2Sus01 = noData[:finIt,0+12,1]
comp2Sus11 = noData[:finIt,1+12,1]
comp2Sus21 = noData[:finIt,2+12,1]
comp2Sus02 = noData[:finIt,0+12+9,1]
comp2Sus12 = noData[:finIt,1+12+9,1]
comp2Sus22 = noData[:finIt,2+12+9,1]
comp2Inf01 = noData[:finIt,0+12+3,1]
comp2Inf11 = noData[:finIt,1+12+3,1]
comp2Inf21 = noData[:finIt,2+12+3,1]
comp2Inf02 = noData[:finIt,0+12+9+3,1]
comp2Inf12 = noData[:finIt,1+12+9+3,1]
comp2Inf22 = noData[:finIt,2+12+9+3,1]
comp2Rec01 = noData[:finIt,0+12+6,1]
comp2Rec11 = noData[:finIt,1+12+6,1]
comp2Rec21 = noData[:finIt,2+12+6,1]
comp2Rec02 = noData[:finIt,0+12+9+6,1]
comp2Rec12 = noData[:finIt,1+12+9+6,1]
comp2Rec22 = noData[:finIt,2+12+9+6,1]

comp1Rec0 = noData[:finIt,6,0]
comp2Rec0 = noData[:finIt,6,1]
comp3Rec0 = noData[:finIt,6,2]
comp1Rec1 = noData[:finIt,7,0]
comp2Rec1 = noData[:finIt,7,1]
comp3Rec1 = noData[:finIt,7,2]
comp1Rec2 = noData[:finIt,8,0]
comp2Rec2 = noData[:finIt,8,1]
comp3Rec2 = noData[:finIt,8,2]

comp3Sus01 = noData[:finIt,0+12,2]
comp3Sus11 = noData[:finIt,1+12,2]
comp3Sus21 = noData[:finIt,2+12,2]
comp3Sus02 = noData[:finIt,0+12+9,2]
comp3Sus12 = noData[:finIt,1+12+9,2]
comp3Sus22 = noData[:finIt,2+12+9,2]
comp3Inf01 = noData[:finIt,0+12+3,2]
comp3Inf11 = noData[:finIt,1+12+3,2]
comp3Inf21 = noData[:finIt,2+12+3,2]
comp3Inf02 = noData[:finIt,0+12+9+3,2]
comp3Inf12 = noData[:finIt,1+12+9+3,2]
comp3Inf22 = noData[:finIt,2+12+9+3,2]
comp3Rec01 = noData[:finIt,0+12+6,2]
comp3Rec11 = noData[:finIt,1+12+6,2]
comp3Rec21 = noData[:finIt,2+12+6,2]
comp3Rec02 = noData[:finIt,0+12+9+6,2]
comp3Rec12 = noData[:finIt,1+12+9+6,2]
comp3Rec22 = noData[:finIt,2+12+9+6,2]

comp1Dead0 = noData[:finIt,9,0]
comp2Dead0 = noData[:finIt,9,1]
comp3Dead0 = noData[:finIt,9,2]
comp1Dead1 = noData[:finIt,10,0]
comp2Dead1 = noData[:finIt,10,1]
comp3Dead1 = noData[:finIt,10,2]
comp1Dead2 = noData[:finIt,11,0]
comp2Dead2 = noData[:finIt,11,1]
comp3Dead2 = noData[:finIt,11,2]

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp1Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp1Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp1Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp1Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp1Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp1Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp1Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp1Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp1Dead0, label="Dead0")
line4,=ax.plot(timeData,comp1Dead1, label="Dead1")
line4,=ax.plot(timeData,comp1Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp1Sus0+comp1Sus1+comp1Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Inf0+comp1Inf1+comp1Inf2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Rec0+comp1Rec1+comp1Rec2, label="Susceptible total")
line1,=ax.plot(timeData,comp1Dead0+comp1Dead1+comp1Dead2, label="Susceptible total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 1 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()



fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp2Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp2Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp2Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp2Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp2Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp2Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp2Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp2Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp2Dead0, label="Dead0")
line4,=ax.plot(timeData,comp2Dead1, label="Dead1")
line4,=ax.plot(timeData,comp2Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()

fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp2Sus0+comp2Sus1+comp2Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp2Inf0+comp2Inf1+comp2Inf2, label="Infectious total")
line1,=ax.plot(timeData,comp2Rec0+comp2Rec1+comp2Rec2, label="Recovered total")
line1,=ax.plot(timeData,comp2Dead0+comp2Dead1+comp2Dead2, label="Dead total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 2 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus0, label="Susceptible0")
line1,=ax.plot(timeData,comp3Sus1, label="Susceptible1")
line1,=ax.plot(timeData,comp3Sus2, label="Susceptible2")
line2,=ax.plot(timeData,comp3Inf0, label="Infectious0")
line2,=ax.plot(timeData,comp3Inf1, label="Infectious1")
line2,=ax.plot(timeData,comp3Inf2, label="Infectious2")
line3,=ax.plot(timeData,comp3Rec0, label="Recovered0")
line3,=ax.plot(timeData,comp3Rec1, label="Recovered1")
line3,=ax.plot(timeData,comp3Rec2, label="Recovered2")
line4,=ax.plot(timeData,comp3Dead0, label="Dead0")
line4,=ax.plot(timeData,comp3Dead1, label="Dead1")
line4,=ax.plot(timeData,comp3Dead2, label="Dead2")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()


fig, ax = plt.subplots(figsize=(15,5))
line1,=ax.plot(timeData,comp3Sus0+comp3Sus1+comp3Sus2, label="Susceptible total")
line1,=ax.plot(timeData,comp3Inf0+comp3Inf1+comp3Inf2, label="Infectious total")
line1,=ax.plot(timeData,comp3Rec0+comp3Rec1+comp3Rec2, label="Recovered total")
line1,=ax.plot(timeData,comp3Dead0+comp3Dead1+comp3Dead2, label="Dead total")
legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for compartment 3 visitation')
plt.xlabel('Time (days)')
plt.ylabel('Individuals')

plt.show()









