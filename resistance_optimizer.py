'''
Python version: 3.5
Author: Israel Flores
Discription: This program finds/combines a desired resistance among a finite number of resistors.
The resistor values should be located in another file named “myResistors.txt”. The formatting of
that text file should (in every line) have the resistor value, followed by a comma, and then
followed by the quantity. For example, if you have two 330 ohm, five 1kilo-ohm, and three 150
ohm resistors, your file should look like this:

330,2
1000,5
150,3

This program is free software.

'''
import numpy as np
import abc 
import sys

# base class for two child/sub-classes (SingleResistor and CompositeResistor)
class Resistance(metaclass=abc.ABCMeta):
# The strSchematic string variable gives instructions on how to connect/build the
# the overall resistance. Resistors A and B are connected in series with the notation: [A,B].
# A parallel connection uses this notation: (A;B). Any composite resistance can be
# built using combinations of these two connections.
    def __init__(self, totalResistance, strSchematic):
        self.__totalResistance = totalResistance
        self.__strSchematic = strSchematic
    
    def getTotalResistance(self):
        return self.__totalResistance  
        
    def getStrSchematic(self):
        return self.__strSchematic
        
# This method converts strSchematic into a schematic-like drawing and displays it in the console 
    def showResistorConnections(self):
        s = self.__strSchematic
        resStrLength = len("---<1.000E+00>---")
        schematic = ["",""]
        x, y = 0, 0
        stackX, stackY = [], []
        readingNumbers = False
           
        for c in range(len(s)): 
            if readingNumbers == True and s[c] != '>':
                schematic[y] += s[c]
            elif s[c] == '(':
                stackX.append(x)        
            elif s[c] == '<':            
                schematic[y] += "---<"   
                readingNumbers = True
            elif s[c] == '>':            
                schematic[y] += ">---"   
                readingNumbers = False
                x += 1
            elif s[c] == ';':
                x = stackX.pop()
                stackY.append(y)
                schematic.extend(("", ""))
                y += 2            
                
                for n in range(x):
                    for leng in range(resStrLength):
                        schematic[y-1] += " "                    
                schematic[y-1] += "|"
                
                for n in range(y-2, 0, -1):
                    if schematic[n][12*x] != ' ': break
                    else: schematic[n] = schematic[n][:resStrLength*x] + "|" + schematic[n][resStrLength*x+1:]            
                
                for n in range(x):
                    for leng in range(resStrLength):
                        schematic[y] += " " 
            elif s[c] == ')': 
                y_rightConnection = stackY.pop()                   
                lengthUpper = len(schematic[y_rightConnection])  
                lengthLower = len(schematic[y])
                deltaLength = lengthUpper - lengthLower
                maxLength = lengthUpper if lengthUpper > lengthLower else  lengthLower  
                
                if maxLength == lengthUpper:
                    for n in range(deltaLength):
                        schematic[y] += "-"
                    x = (len(schematic[y]))//resStrLength 
                else:
                    for n in range(abs(deltaLength)):
                        schematic[y_rightConnection] += "-"   
                                  
                for n in range(y_rightConnection, y):
                    if len(schematic[n]) < maxLength: 
                        while len(schematic[n]) < (maxLength - 1):
                            schematic[n] += " "
                        schematic[n] += "|"                         
        schematic[0] = "O---" + schematic[0]
        for n in range(1, len(schematic)):
            schematic[n] = "    " + schematic[n]       
        schematic[-2] += "---O"  
        for line in schematic:
            print(line)
            
    @abc.abstractmethod
    def makeStrSchematic(self): pass
    
    @abc.abstractmethod
    def getInstanceResArray(self): pass
##################### end of abstract Resistance base class #############################  
            
class SingleResistor(Resistance):
    
#every time an instance is created, its totalResistance will be appended into this array
    __allResistors = np.array([])
    
    def __init__(self, totalResistance, quantity=1):           
        super().__init__(totalResistance, self.makeStrSchematic(totalResistance))
        self.__quantity = quantity
        self.__updateClassResistors(totalResistance, quantity)
        
    def makeStrSchematic(self, res):
        return '<' + '{:.03E}'.format(res) + '>'     
#returns totalResistance in np.array form (useful for certain operations like concantinating arrays)
    def getInstanceResArray(self):
        return np.array([self.getTotalResistance()])       
        
    def getQuantity(self):
        return self.__quantity    
#i.e. update _allResistors class array
    def __updateClassResistors(self, res, quant):
        for n in range(quant):
            SingleResistor.__allResistors = np.append(SingleResistor.__allResistors,np.array([res]))
            
    @classmethod
    def getClassResArray(cls):
        return cls.__allResistors    
   
        
class CompositeResistor(Resistance):
    def __init__(self, totalResistance, strSchem1,  strSchem2, array1, array2, connect):
        super().__init__(totalResistance, self.makeStrSchematic(strSchem1, strSchem2, connect))
        self.__resistors = np.concatenate((array1, array2))
    
    def makeStrSchematic(self, s1, s2, connect):
        if connect == 'S': return '[{},{}]'.format(s1, s2)
        else:              return '({};{})'.format(s1, s2)
    
    def getInstanceResArray(self):
        return self.__resistors
  
    @classmethod #alternative constructor 1
    def series(cls, r1, r2):
        return cls(r1.getTotalResistance() + r2.getTotalResistance(), r1.getStrSchematic(), \
        r2.getStrSchematic(), r1.getInstanceResArray(), r2.getInstanceResArray(), 'S')
        
    @classmethod #alternative constructor 2
    def parallel(cls, r1, r2):
        return cls(1/(1/r1.getTotalResistance() + 1/r2.getTotalResistance()) \
        , r1.getStrSchematic(), r2.getStrSchematic(), r1.getInstanceResArray(), r2.getInstanceResArray(), 'P')  

'''This function takes a dictionary (with resistor-objects as values and the  object's totalResistance
as keys) and a desired resistance as its inputs . It returns the object with the closest totalResistance
to the desired resistance.'''  
def findBest(d, disiredRes):
    closestObject = next(iter(dict.values(d)))
    for key, value in d.items():
        if abs(disiredRes - key) < abs(disiredRes - closestObject.getTotalResistance()): closestObject = value
    return closestObject
''' This function takes in the instance arrays from two resistor-objects and checks if their combined
resistors form enough to make a new object (i.e. enough in  __allResistors)''' 
def isThereEnoughRes(a1, a2):         
    temp = np.copy(a2)        
    for n in a1:
        index = np.where(temp==n)
        if len(index[0]) == 0: return False
        else: temp[index[0][0]] = -1
    return True  

def isResWithinPercentRange(obj, desired, percent):    
    if abs(obj.getTotalResistance() - desired)/desired <= percent/100: return True
    else: return False 
    
#This function prints an object's schematic, totalResistance, desiredResistance, and the % difference. 
def printStuff(obj, desired):
    obj.showResistorConnections()
    percDiff = '{:.3f}'.format(100*(obj.getTotalResistance() - desired)/desired)
    resistance = '{:.2f}'.format(obj.getTotalResistance(),)
    print('This resistance = {} ohms (desired = {} ohms), difference = {}% \n\n\n\n\n'.format(resistance, \
          desired, percDiff)) 
      
''' The rList parameter in this function is a list with length=1 and a dictionary in its zero/only index. 
The dictionary in rList consists of SingleResistor objects (values) and the object's totalResistance (keys).
The function returns a list of resistor objects called "optimalList". The zero-index of optimalList contains the
global optimal object (i.e. the object with the closest totalResistance to a desired resistance). After that, the
indices of optimalList correspond to the best object using the same number of resistors as the corresponding 
index. For example, index 3 of optimalList (if it exists) contains the optimal object using exaclty 3 resistors
(i.e. it's a local optimum) '''      
def getOptimalList(rList, desiredR, maxR, percentage):    
    optimalList = [None] #reserve the zero index for global optimum  
    
    print("Finding best combination with 1 resistor...\n")    
    for singleResObject in rList[0].values():
        if isResWithinPercentRange(singleResObject, desiredR, percentage):
            optimalList[0] = singleResObject
            return optimalList 
    optimalList.append(findBest(rList[0], desiredR))
    printStuff(optimalList[-1], desiredR)
        
    for n in range(maxR - 1):
        maxSteps = len(rList)//2
        rList.append({})        
        print("Finding best combination with {} resistors...\n".format((n+2)))
        for step in range(maxSteps+1):
            for ob1 in rList[step].values():
                for ob2 in rList[len(rList)-step-2].values():
                    if isThereEnoughRes(np.concatenate((ob1.getInstanceResArray(), ob2.getInstanceResArray())), \
                        SingleResistor.getClassResArray()):  
                        
                        newSeries = CompositeResistor.series(ob1, ob2)
                        if isResWithinPercentRange(newSeries, desiredR, percentage):
                            optimalList[0] = newSeries
                            return optimalList 
                        doesNewSerExist = False
                        for index in range(len(rList)):
                            if newSeries.getTotalResistance() in rList[index]:
                                doesNewSerExist = True
                                break                                
                        if doesNewSerExist == False:                   
                            rList[len(rList)-1][newSeries.getTotalResistance()] = newSeries                        
                        
                        newParallel = CompositeResistor.parallel(ob1, ob2)
                        if isResWithinPercentRange(newParallel, desiredR, percentage):
                            optimalList[0] = newParallel
                            return optimalList
                        doesNewParExist = False
                        for index in range(len(rList)):
                            if newParallel.getTotalResistance() in rList[index]:
                                doesNewParExist = True
                                break                
                        if doesNewParExist == False:                     
                            rList[len(rList)-1][newParallel.getTotalResistance()] = newParallel                            
        optimalList.append(findBest(rList[n+1], desiredR))
        printStuff(optimalList[-1], desiredR)
    
    bestDict = {}
    for n in range(1, len(optimalList)):
        bestDict[optimalList[n].getTotalResistance()] = optimalList[n]
    optimalList[0] = findBest(bestDict, desiredR)
    
    return optimalList

#declare a dictionary/list for holding our intitial resistors (1st parameter in the getOptimalList function)
rL = [{}]

#get all of the resistors that we'll have to work with via a file named "myResistors.txt"
try:
    with open('myResistors.txt', 'r') as f:
        line = f.readline()
        while len(line) > 0: 
            a,b = line.split(',')
            rL[0][float(a)] = SingleResistor(float(a), int(b))
            line = f.readline()
except ValueError:
    print("Please make sure that your myResistors.txt file is properly formatted. Every line in "
    "the file should contain a resistor-value followed by its quantity and separated by a comma.") 
    sys.exit()
except FileNotFoundError:
    print("Your file was not found. Make sure that your file is named myResistors.txt and that "
    "it's located in the same directory as this program. ")
    sys.exit()   

#get user's desired resistance
while(True):
    try:
        desiredResistance = float(input("Enter your disired resistance: "))
        if desiredResistance <= 0: raise ValueError
    except ValueError: print("(Your desired resistance must be a number and greater than zero.)")
    else: break

#get user's maximumResistors
while(True):
    try:
        maximumResistors = int(input("Enter the maximum number of resistors that you're willing to use/combine: ")) 
        if maximumResistors <= 0 or maximumResistors > len(SingleResistor.getClassResArray()): raise ValueError
    except ValueError:
        print("(The number of max resistors must be an integer in between 1 and the total number "
        "of all your resistors (i.e. {} in this case).".format(len(SingleResistor.getClassResArray())))
    else: break

#get user's stopping percentage
while(True):
    try:
        stoppingPercentage = float(input("Finally, enter the stopping percentage (the program will "
        "stop once it finds a resisitance within this range): "))
        if stoppingPercentage < 0 or stoppingPercentage > 100: raise ValueError
    except ValueError: print("(The percentage must be a number and between zero and one hundred.)")
    else:
        print("\n\n")
        break
    
#find glabal and/or local optimum solution(s)   
myOptimalList = getOptimalList(rL, desiredResistance, maximumResistors, stoppingPercentage)

print("Search complete. The closest match uses {} resistor(s):\n".format(len(myOptimalList[0].getInstanceResArray())))

#print the final answer
printStuff(myOptimalList[0], desiredResistance)

#%%########################## END ############################################