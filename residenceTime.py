#This file contains the neccecary code to run simulations for the
#residence time model

#import neccecary libraries
import numpy as np
import matplotlib.pyplot as plt
import math
import random

#define functions we will use later
def calculatePropensityTotal(ruleList,compartment,time,constForLatent):
    timeCatagory = (math.floor(time*24))%24
    total = 0
    for rule in ruleList:
        total = total+rule.calculatePropensity(compartment,timeCatagory,time,constForLatent)
      
    return(total)
    

#define functions to be passed as kinetic functions later    
def infection(location,profiles,profile1,profile2,infectionRates,timeCatagory,compartmentP,time,constForLatent):
    #print(profiles[profile1][timeCatagory],profiles[profile2][timeCatagory],location)
    day = math.floor(time)
    
    if day%7 == 5 or day%7==6:
        retVal = 0.2/550
        
    if ((profiles[profile1][timeCatagory]==location) and (profiles[profile2][timeCatagory]==location)):
        retVal = infectionRates[location]
        divVal = compartmentP.initPop

                
        retVal = retVal/divVal
        
    else:
        retVal = 0
        
    return(retVal)
        
def infectionTotal(profiles,profile1,profile2,infectionRates,timeCatagory,compartment,noOfLocations,time,constForLatent):
    total = 0
    for i in range(0,noOfLocations):
        total = total+infection(i,profiles,profile1,profile2,infectionRates,timeCatagory,compartment,time,constForLatent)
            
    return(total)

def recovery(location,profiles,profile1,profile2,recoveryRates,timeCatagory,compartment,time,constForLatent):
    if (profiles[profile1][timeCatagory]==location) :
        retVal = recoveryRates[location]
        
        
    else:
        retVal = 0
        
    return(retVal)
        
def recoveryTotal(profiles,profile1,profile2,recoveryRates,timeCatagory,compartment,noOfLocations,time,constForLatent):
    total = 0
    for i in range(0,noOfLocations):
        total = total+recovery(i,profiles,profile1,profile2,recoveryRates,timeCatagory,compartment,time,constForLatent)
            
    return(total)


def death(location,profiles,profile1,profile2,deathRates,timeCatagory,compartment,time,constForLatent):
    if (profiles[profile1][timeCatagory]==location) :
        retVal = deathRates[location]
        
        
    else:
        retVal = 0
        
    return(retVal)
        
def deathTotal(profiles,profile1,profile2,deathRates,timeCatagory,compartment,noOfLocations,time,constForLatent):
    total = 0
    for i in range(0,noOfLocations):
        total = total+death(i,profiles,profile1,profile2,deathRates,timeCatagory,compartment,time,constForLatent)
            
    return(total)

    
def loss(location,profiles,profile1,profile2,lossRates,timeCatagory,compartment,time,constForLatent):
    if (profiles[profile1][timeCatagory]==location) :
        retVal = lossRates[location]
 
    else:
        retVal = 0
        
    return(retVal)
        
def lossTotal(profiles,profile1,profile2,lossRates,timeCatagory,compartment,noOfLocations,time,constForLatent):
    total = 0
    for i in range(0,noOfLocations):
        total = total+loss(i,profiles,profile1,profile2,lossRates,timeCatagory,compartment,time,constForLatent)
            
    return(total)   


def latent(location,profiles,profile1,profile2,lossRates,timeCatagory,compartment,time,constForLatent):
    
    if (profiles[profile1][timeCatagory]==location) :
        if location==0 or location==6:
            retVal=0
        else:
            retVal = constForLatent[location]
    else:
        retVal=0
        
    #return(0)
    return(retVal/550)



def latentTotal(profiles,profile1,profile2,lossRates,timeCatagory,compartment,noOfLocations,time,constForLatent):
    total = 0
    for i in range(0,noOfLocations):
        total = total+latent(i,profiles,profile1,profile2,lossRates,timeCatagory,compartment,time,constForLatent)
            
    return(total)   

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
    else:
        return(factorial(n)/(factorial(r)*factorial(n-r)))
    
   #define rule class 
class rule:
    #seperateing kineticCOnst and kineticFunct may not be neccecary for computational
    #efficiancy
    def __init__(self,sourceComplex,targetComplex,kineticFunct,profiles,profile1,profile2,rates,noOfLocations):
        self.sourceComplex = sourceComplex
        self.targetComplex = targetComplex
        self.kineticFunct = kineticFunct
        self.profiles = profiles
        self.profile1 = profile1
        self.profile2 = profile2
        self.rates = rates
        self.noOfLocations = noOfLocations
        self.propensity = 0
        

    def executeRule(self,compartment):
        
        for i in range(0,compartment.noTypes):
            compartment.typeList[i] = compartment.typeList[i] - self.sourceComplex[i] + self.targetComplex[i]
            

    def calculatePropensity(self,compartment,timeCatagory,time,constForLatent):
        total = self.kineticFunct(self.profiles,self.profile1,self.profile2,self.rates,timeCatagory,compartment,self.noOfLocations,time,constForLatent)
        for i in range(0,compartment.noTypes):
            total = total*(ncr(compartment.typeList[i],self.sourceComplex[i]))

        return(total)
            
    def printSelf(self):
        print(self.sourceComplex)
        print(self.targetComplex)
            
            
#define a compartment
class compartment:
    def __init__(self,typeList):

        self.typeList = typeList
        self.noTypes = len(typeList)
        self.initPop = self.getPopulation()

        
    def getPopulation(self):
        total = 0
        for type in self.typeList:
            total = total+type
            
        return(total)
        

#code for gillespie adaptation
def gillespie(compartment,ruleList,finTime,maxIts,increment):
    
    noTypes = compartment.noTypes
    time = 0
    data = np.zeros((maxIts+1,noTypes))
    timeData = np.zeros(maxIts+1)

    iteration = 0
    
    #these parameters must be changed by hand
    sumForLatent = [0,0,0,0,0,0,0]
    constForLatent = [0,0,0,0,0,0,0]
    
    ca=0.5
    beta1=0.1
    beta2=0.1
    
    

    while time<finTime and  iteration<maxIts:

        #print(time)        

        iteration = iteration+1
        
        
        r2 = np.random.uniform(0,1)
        r1 = np.random.uniform(0,1)
        
        # incrementNo = 0
        # baseTime = time
        
        # startingIncrement = math.floor(time*24)/24
        
        # thisIncrementPropSum = calculatePropensityTotal(ruleList, compartment, time)
        # #print(thisIncrementPropSum)
        
        
        
        # newTime = -math.log(r1)/thisIncrementPropSum
        
        # print(newTime)
        # #print(newTime)
        # #newTime = time
        
        
        
        # while (newTime>(incrementNo+1)*increment):
            
        #     lastIncrementPropSum = thisIncrementPropSum
            
        #     incrementNo = incrementNo+1
            
        #     thisIncrementPropSum = calculatePropensityTotal(ruleList, compartment, incrementNo*increment+baseTime)

            
            
        #     if incrementNo==1:
                
        #         newTime = (startingIncrement+incrementNo)*increment-baseTime - (math.log(r1)+((startingIncrement+1)*increment-baseTime)*lastIncrementPropSum)/thisIncrementPropSum
        #     else:
                
        #         newTime = (startingIncrement+incrementNo)*increment-baseTime + (newTime-((startingIncrement+incrementNo-1)*increment-baseTime))*(lastIncrementPropSum/thisIncrementPropSum)-(increment*lastIncrementPropSum)/thisIncrementPropSum
         
        # time = time+newTime
        
        
        
        
        
        
        
        incrementNo = 0
        baseTime = time
        
        startingIncrement = math.floor(time*24)
        
        
        thisIncrementPropSum = calculatePropensityTotal(ruleList, compartment, time,constForLatent)
        #print(thisIncrementPropSum)
        
        if thisIncrementPropSum==0:
            return(data,timeData,iteration)
            
        
        newTime = -math.log(r1)/thisIncrementPropSum
        #print(newTime)
        #newTime = time
        
        noIncrements = 0
        
        while (newTime+time>(startingIncrement+incrementNo+1)*increment):
            
            noIncrements = noIncrements+1
            
            # print("incrementNo",incrementNo)
            # print("time",time)
            # print("aprox time",startingIncrement*increment)
            # print("new time",newTime+time)
            # print("next increment (tested)",(startingIncrement+incrementNo+1)*increment)
            
            lastIncrementPropSum = thisIncrementPropSum
            
            incrementNo = incrementNo+1
            
            thisIncrementPropSum = calculatePropensityTotal(ruleList, compartment, (startingIncrement+incrementNo)*increment,constForLatent)

            
            
            if incrementNo==1:
                
                newTime = (startingIncrement+incrementNo)*increment-baseTime - (math.log(r1)+((startingIncrement+1)*increment-baseTime)*lastIncrementPropSum)/thisIncrementPropSum
            else:
                
                newTime = (startingIncrement+incrementNo)*increment-baseTime + (newTime-((startingIncrement+incrementNo-1)*increment-baseTime))*(lastIncrementPropSum/thisIncrementPropSum)-(increment*lastIncrementPropSum)/thisIncrementPropSum
         
        time = time+newTime
        
        prevInf = [0,0,0,0,0,0,0]
        
        if noIncrements>0:
        
        
            incrementNo = 0
            while incrementNo<noIncrements:
            
                if incrementNo==0:
                    
                    oldTimeStep = time-newTime
                    
                    incrementNo = incrementNo+1
                    
                    newTimeStep = (startingIncrement+incrementNo)*increment
                                    
                    
                elif incrementNo==noIncrements:
    
                    oldTimeStep = (startingIncrement+incrementNo)*increment
                    
                    incrementNo = incrementNo+1
                    
                    newTimeStep = time
                    
                    
                else:
                    
                    oldTimeStep = (startingIncrement+incrementNo)*increment
                    
                    incrementNo = incrementNo+1
                    
                    newTimeStep = (startingIncrement+incrementNo)*increment
                    
    
                for location in range(0,noLocations):
             
                    prevInf[location] = 0
                    for rClass in range(0,noClasses):
                        if profiles[rClass][(startingIncrement+incrementNo)%24]==location:
                            prevInf[location] = prevInf[location]+compartment.typeList[4*i+1]
    
                    
    
                    sumForLatent[location] = sumForLatent[location] + (ca*beta1)*((prevInf[location]/(ca*beta2))*(math.exp(ca*beta2*newTimeStep)-math.exp(ca*beta2*oldTimeStep)))
                    if((1/math.exp(ca*beta1*time))*sumForLatent[location])<0:
                        constForLatent[location] = 0
                    else:
                        constForLatent[location] = (1/math.exp(ca*beta1*time))*sumForLatent[location]
                                                                                               
                                                                                  
    
        else:
            oldTimeStep = time-newTime

            newTimeStep = time
                    
            for location in range(0,noLocations):
         
                prevInf[location] = 0
                for rClass in range(0,noClasses):
                    if profiles[rClass][(startingIncrement+incrementNo)%24]==location:
                        prevInf[location] = prevInf[location]+compartment.typeList[4*i+1]

                sumForLatent[location] = sumForLatent[location] + (ca*r1)*((prevInf[location]/(ca*r2))*(math.exp(ca*r2*newTimeStep)-math.exp(ca*r2*oldTimeStep)))
                #print((1/math.exp(ca*r1*time))*sumForLatent[location])
                if((1/math.exp(ca*r1*time))*sumForLatent[location])<0:
                    constForLatent[location] = 0
                else:
                    constForLatent[location] = (1/math.exp(ca*r1*time))*sumForLatent[location]
               

    
        
        target = r2*calculatePropensityTotal(ruleList, compartment, time,constForLatent)
        
        currentTotal = 0
        currentIndex = 0
        found = False
        #print("target:",target)
        while not(found):
            #print(currentTotal)
            if currentTotal<target<=currentTotal+ruleList[currentIndex].calculatePropensity(compartment,(math.floor(time*24))%24,time,constForLatent):
                found = True
            else:
                currentTotal = currentTotal+ruleList[currentIndex].calculatePropensity(compartment,(math.floor(time*24))%24,time,constForLatent)
                currentIndex = currentIndex+1




        ruleList[currentIndex].executeRule(compartment)
        
        

        
        
        
        data[iteration-1,:] = compartment.typeList
        
        timeData[iteration-1] = time

    return(data,timeData,iteration)
                    


#code to initialise each type of simulation is below. One must
#comment out the blocks they do not wish to use

#residence profiles

#small town
# noClasses = 11
# noLocations = 6

# profiles = [
#     [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,4,4,5,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,5,0,0,0,4,4,4,0,0],
#     [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,5,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,4,4,5,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,5,0,4,4,4,0,0],
#     [0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,5,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,4,4,4,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,4,4,4,5,5,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,4,4,4,0,0,0,0,0,0]
#     ]



#school
noClasses = 12
noLocations = 7
#schedule 2
profiles = [
    [1,1,6,6 ,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,6 ,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,6,1,6 ,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [6,6,2,6 ,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [6,6,2,6 ,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,3,3,6 ,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    
    [4,4,6,6 ,6,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,5,4,6 ,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,6,6,6 ,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [6,4,6,6 ,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [6,3,3,6 ,6,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [5,4,4,6 ,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
    ]


#schedule 1
# profiles = [
#     [1,3,6,6 ,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [1,3,6,6 ,6,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [4,6,6,6 ,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [6,1,6,6 ,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [1,1,5,6 ,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [2,2,5,6 ,4,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    
#     [5,6,2,6 ,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [6,1,6,6 ,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [6,1,3,6 ,4,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [5,6,3,6 ,6,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [6,2,2,6 ,6,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [5,5,6,6 ,3,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
#     ]


#location based parameters

#school
infectionRates = [0,10,10,10,10,10,0.1]
recoveryRates = [0.05,0.05,0.05,0.05,0.05,0.05,0.05]
deathRates = [0.02,0.02,0.02,0.02,0.02,0.02,0.02]
lossRates = [0.005,0.005,0.005,0.005,0.005,0.005,0.005]



#small town
# infectionRates = [0.2,0.7,0.5,0.6,2,0.6]
# recoveryRates = [0.06,0.06,0.06,0.06,0.06,0.06]
# deathRates = [0.01,0.01,0.01,0.01,0.01,0.01]
# lossRates = [0.005,0.005,0.005,0.005,0.005,0.005]

#initial conditions

#school
compartmentP = compartment([13,2,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0,
                            15,0,0,0
                            ])

#small town
# compartmentP = compartment([50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             45,5,0,0,
#                             50,0,0,0,
#                             50,0,0,0,
#                             ])

#rules

ruleList = []

for i in range(0,noClasses):
    for j in range(0,noClasses):
        sourceComplex = []
        targetComplex = []
        for k in range(0,noClasses*4):
            sourceComplex.append(0)
            targetComplex.append(0)
        
        if i==j:
            sourceComplex[i*4]=1
            sourceComplex[j*4+1]=1
            targetComplex[j*4+1]=2
        else:
            sourceComplex[i*4]=1
            sourceComplex[j*4+1]=1
            targetComplex[i*4+1]=1
            targetComplex[j*4+1]=1
            
        ruleList.append(rule(sourceComplex, targetComplex, infectionTotal, profiles, i, j, infectionRates,noLocations))
        
        
for i in range(0,noClasses):

    sourceComplex = []
    targetComplex = []
    for k in range(0,noClasses*4):
        sourceComplex.append(0)
        targetComplex.append(0)
    
    sourceComplex[i*4+1]=1
    targetComplex[i*4+2]=1
    
    ruleList.append(rule(sourceComplex, targetComplex, recoveryTotal, profiles, i,j, recoveryRates,noLocations))
    
    
for i in range(0,noClasses):

    sourceComplex = []
    targetComplex = []
    for k in range(0,noClasses*4):
        sourceComplex.append(0)
        targetComplex.append(0)
    

    sourceComplex[i*4+1]=1
    targetComplex[i*4+3]=1
    
    ruleList.append(rule(sourceComplex, targetComplex, deathTotal, profiles, i, j, deathRates,noLocations))
    
for i in range(0,noClasses):

    sourceComplex = []
    targetComplex = []
    for k in range(0,noClasses*4):
        sourceComplex.append(0)
        targetComplex.append(0)
    

    sourceComplex[i*4+2]=1
    targetComplex[i*4]=1

    ruleList.append(rule(sourceComplex, targetComplex, lossTotal, profiles, i, j, lossRates,noLocations))     


#latent infection rule, exclude if you wish to simulate without latent infection

for i in range(0,noClasses):

    sourceComplex = []
    targetComplex = []
    for k in range(0,noClasses*4):
        sourceComplex.append(0)
        targetComplex.append(0)
    

    sourceComplex[i*4+0]=1
    targetComplex[i*4+1]=1

    ruleList.append(rule(sourceComplex, targetComplex, latentTotal, profiles, i, j, lossRates,noLocations))     




#code to plot results. for ths schools, class 12 must be included, for 
#small town excluded

gillespieData = gillespie(compartmentP,ruleList,100,10000,1/24)

noData = gillespieData[0]
timeDataUncut = gillespieData[1]
finIt = gillespieData[2]

class1Sus = noData[:finIt,0]

class1Inf = noData[:finIt,1]

class1Rec = noData[:finIt,2]

class1Dead = noData[:finIt,3]


class2Sus = noData[:finIt,4]

class2Inf = noData[:finIt,5]

class2Rec = noData[:finIt,6]

class2Dead = noData[:finIt,7]


class3Sus = noData[:finIt,8]

class3Inf = noData[:finIt,9]

class3Rec = noData[:finIt,10]

class3Dead = noData[:finIt,11]


class4Sus = noData[:finIt,12]

class4Inf = noData[:finIt,13]

class4Rec = noData[:finIt,14]

class4Dead = noData[:finIt,15]


class5Sus = noData[:finIt,16]

class5Inf = noData[:finIt,17]

class5Rec = noData[:finIt,18]

class5Dead = noData[:finIt,19]


class6Sus = noData[:finIt,20]

class6Inf = noData[:finIt,21]

class6Rec = noData[:finIt,22]

class6Dead = noData[:finIt,23]


class7Sus = noData[:finIt,24]

class7Inf = noData[:finIt,25]

class7Rec = noData[:finIt,26]

class7Dead = noData[:finIt,27]


class8Sus = noData[:finIt,28]

class8Inf = noData[:finIt,29]

class8Rec = noData[:finIt,30]

class8Dead = noData[:finIt,31]


class9Sus = noData[:finIt,32]

class9Inf = noData[:finIt,33]

class9Rec = noData[:finIt,34]

class9Dead = noData[:finIt,35]


class10Sus = noData[:finIt,36]

class10Inf = noData[:finIt,37]

class10Rec = noData[:finIt,38]

class10Dead = noData[:finIt,39]


class11Sus = noData[:finIt,40]

class11Inf = noData[:finIt,41]

class11Rec = noData[:finIt,42]

class11Dead = noData[:finIt,43]


class12Sus = noData[:finIt,44]

class12Inf = noData[:finIt,45]

class12Rec = noData[:finIt,46]

class12Dead = noData[:finIt,47]


timeData = timeDataUncut[:finIt]


#school plots

fig, ax = plt.subplots(figsize=(15,5))
line,=ax.plot(timeData,class1Inf, label="Student type 1")
line,=ax.plot(timeData,class2Inf, label="Student type 2")
line,=ax.plot(timeData,class3Inf, label="Student type 3")
line,=ax.plot(timeData,class4Inf, label="Student type 4")
line,=ax.plot(timeData,class5Inf, label="Student type 5")
line,=ax.plot(timeData,class6Inf, label="Student type 6")

legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for first half of residence profiles')
plt.xlabel('Time (days)')
plt.ylabel('Infectious individuals')

plt.show()




fig, ax = plt.subplots(figsize=(15,5))
line,=ax.plot(timeData,class7Inf, label="Student type 7")
line,=ax.plot(timeData,class8Inf, label="Student type 8")
line,=ax.plot(timeData,class9Inf, label="Student type 9")
line,=ax.plot(timeData,class10Inf, label="Student type 10")
line,=ax.plot(timeData,class11Inf, label="Student type 11")
line,=ax.plot(timeData,class12Inf, label="Student type 12")



legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Simulation for second half of residence profiles')
plt.xlabel('Time (days)')
plt.ylabel('Infectious individuals')

plt.show()



fig, ax = plt.subplots(figsize=(15,5))
# line,=ax.plot(timeData,class1Sus+class2Sus+class3Sus+class4Sus+class5Sus+class6Sus+class7Sus+class8Sus, label="Total susceptible population")
# line,=ax.plot(timeData,class1Inf+class2Inf+class3Inf+class4Inf+class5Inf+class6Inf+class7Inf+class8Inf, label="Total infectious population")
# line,=ax.plot(timeData,class1Rec+class2Rec+class3Rec+class4Rec+class5Rec+class6Rec+class7Rec+class8Rec, label="Total recovered population")
# line,=ax.plot(timeData,class1Dead+class2Dead+class3Dead+class4Dead+class5Dead+class6Dead+class7Dead+class8Dead, label="Total dead population")
line,=ax.plot(timeData,class1Inf+class2Inf+class3Inf+class4Inf+class5Inf+class6Inf+class7Inf+class8Inf+class9Inf+class10Inf+class11Inf+class12Inf, label="Total infectious population")

legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

plt.title('Plot of total infectious population with second schedule')
plt.xlabel('Time (days)')
plt.ylabel('Infectious individuals')

plt.show()

#small town plots

# fig, ax = plt.subplots(figsize=(15,5))
# line,=ax.plot(timeData,class1Inf, label="Worker 1")
# line,=ax.plot(timeData,class2Inf, label="Worker 2")
# line,=ax.plot(timeData,class3Inf, label="Worker 3")
# line,=ax.plot(timeData,class4Inf, label="Worker 4")
# line,=ax.plot(timeData,class5Inf, label="Worker 5")
# line,=ax.plot(timeData,class6Inf, label="Worker 6")
# line,=ax.plot(timeData,class7Inf, label="Student 1")
# line,=ax.plot(timeData,class8Inf, label="Student 2")
# line,=ax.plot(timeData,class9Inf, label="Other 1")
# line,=ax.plot(timeData,class10Inf, label="Other 2")
# line,=ax.plot(timeData,class11Inf, label="Other 3")

# legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

# plt.title('Simulation for all residence profiles with latent infection')
# plt.xlabel('Time (days)')
# plt.ylabel('Infectious individuals')

# plt.show()



# fig, ax = plt.subplots(figsize=(15,5))
# line,=ax.plot(timeData,class1Sus+class2Sus+class3Sus+class4Sus+class5Sus+class6Sus+class7Sus+class8Sus+class9Sus+class10Sus+class11Sus, label="Total susceptible population")
# line,=ax.plot(timeData,class1Inf+class2Inf+class3Inf+class4Inf+class5Inf+class6Inf+class7Inf+class8Inf+class9Inf+class10Inf+class11Inf, label="Total infectious population")
# line,=ax.plot(timeData,class1Rec+class2Rec+class3Rec+class4Rec+class5Rec+class6Rec+class7Rec+class8Rec+class9Rec+class10Rec+class11Rec, label="Total recovered population")
# line,=ax.plot(timeData,class1Dead+class2Dead+class3Dead+class4Dead+class5Dead+class6Dead+class7Dead+class8Dead+class9Dead+class10Dead+class11Dead, label="Total dead population")
# #line,=ax.plot(timeData,class1Inf+class2Inf+class3Inf+class4Inf+class5Inf+class6Inf+class7Inf+class8Inf+class9Inf+class10Inf+class11Inf+class12Inf, label="Total infectious population")

# legend = ax.legend(bbox_to_anchor=(1.04,0.5), loc='center left', shadow=True, fontsize='x-large')

# plt.title('Plot of total population dynamics in small town with latent infection')
# plt.xlabel('Time (days)')
# plt.ylabel('Individuals')

# plt.show()












