from LCS_Constants import global_constants
import random
import copy
import math

class Classifier:
    def __init__(self, a=None, b=None, c=None, d=None):
        self.specifiedAttrList = []
        self.condition = []
        self.phenotype = None
        self.fitness = global_constants.init_fit

        self.accuracy = 0.0

        self.initTimeStamp = None

        self.matchCount = 0
        self.correctCount = 0
        
        if isinstance(b, list):
            self.classifierCovering(a,b,c)
        elif isinstance(a, Classifier):
            self.classifierCopy(a,b)
        elif isinstance(a, list) and b == None:
            self.rebootClassifier(a)
        else:
            raise ValueError('Invalid arguments to construct classifier')

    def classifierCovering(self, exploreIter, state, phenotype):

        self.initTimeStamp = exploreIter
        dataInfo = global_constants.env.formatData


        if dataInfo.discretePhenotype:
            self.phenotype = phenotype
        else:
            phenotypeRange = dataInfo.phenotypeList[1] - dataInfo.phenotypeList[0]
            rangeRadius = random.randint(25,75)*0.01 * phenotypeRange/2.0

            Low = float(phenotype) - rangeRadius
            High = float(phenotype) + rangeRadius
            self.phenotype = [Low,High]

        while len(self.specifiedAttrList) < 1:
            for attrRef in range(len(state)):
                if random.random() < global_constants.p_spec and state[attrRef] != cons.labelMissingData:
                    self.specifiedAttrList.append(attrRef)
                    self.condition.append(self.buildMatch(attrRef, state))

    def rebootClassifier(self, classifierList):
        numAttributes = global_constants.env.formatData.numAttributes
        attrInfo = global_constants.env.formatData.attributeInfo

        for attrRef in range(0, numAttributes):
            if classifierList[attrRef] != '#':
                if attInfo[attRef][0]:
                    valueRange = classifierList[attrRef].split(';')
                    self.condition.append(valueRange)
                    self.specifiedAttrList.append(attrRef)
                else:
                    self.condition.append(classifierList[attrRef])
                    self.specifiedAttrList.append(attrRef)

        if global_constants.env.formatData.discretePhenotype:
            self.phenotype = str(classifierList[numAttributes])
        else:
            self.phenotype = classifierList[numAttributes].split(';')
            for i in range(2):
                self.phenotype[i] = float(self.phenotype[i])
        
        self.fitness - float(classifierList[numAttributes + 1])
        self.accuracy = float(classifierList[numAttributes + 2])
        self.initTimeStamp = int(classifierList[numAttributes+6])
        self.correctCount = int(classifierList[numAttributes+9])
        self.matchCount = int(classifierList[numAttributes+10])

    def match(self, state):
        for i in range(len(self.condition)):
            attributeInfo = global_constants.env.formatData.attributeInfo[self.specifiedAttrList[i]]

            if attributeInfo[0]:
                instanceValue = state[self.specifiedAttrList[i]]
                if self.condition[i][0] < instanceValue < self.condition[i][1] or instanceValue == global_constants.labelMissingData:
                    pass
                else:
                    return False
            else:
                stateRep = state[self.specifiedAttrList[i]]
                if stateRep == self.condition[i] or stateRep == global_constants.labelMissingData:
                    pass
                else:
                    return False
        return True

    def buildMatch(self, attrRef, state):
        attributeInfo = global_constants.env.formatData.attributeInfo[attrRef]

        if attributeInfo[0]:
            attrRange = attributeInfo[1][1] - attributeInfo[1][0]
            rangeRadius = random.randint(25,75)*0.01*attrRange/2.0
            Low = state[attrRef] - rangeRadius
            High = state[attrRef] + rangeRadius
            
            condList = [Low, High]
        
        else:
            condList = state[attrRef]

        return condList

    def equals(self, cl):
        if cl.phenotype == self.phenotype and len(cl.specifiedAttrList) == len(self.specifiedAttrList):
            clRefs = sorted(cl.specifiedAttrList)
            selfRefs = sorted(self.specifiedAttrList)
            if clRefs == selfRefs:
                for i in range(len(cl.specifiedAttrList)):
                    tempIndex = self.specifiedAttrList.index(cl.specifiedAttrList[i])
                    if cl.condition[i] == self.condition[tempIndex]:
                        pass
                    else:
                        return False
                return True
        return False


    def updateAccuracy(self):
        self.accuracy = self.correctCount / float(self.matchCount)

    def updateFitness(self):
        if global_constants.env.formatData.discretePhenotype or (self.phenotype[1] - self.phenotype[0])/global_constants.formatData.phenotypeRange < 0.5:
            self.fitness = pow(self.accuracy, global_constants.nu)
        else:
            if (self.phenotype[1] - self.phenotype[0]) >= global_constants.env.formatData.phenotypeRange:
                self.fitness = 0.0
            else:
                self.fitness = math.fabs(pow(self.accuracy, cons.nu) - (self.phenotype[1]-self.phenotype[0])/global_constants.formatData.phenotypeRange)

    def updateExperience(self):
        self.matchCount += 1

    def updateCorrect(self):
        self.correctCount += 1

    def setAccuracy(self, acc):
        self.accuracy = acc

    def setFitness(self, fitness):
        self.fitness = fitness

    def reportClassifier(self):
        numAttributes = global_constants.env.formatData.numAttributes
        thisClassifier = []
        counter = 0
        for i in range(numAttributes):
            if i in self.specifiedAttrList:
                thisClassifier.append(self.condition[counter])
                counter += 1
            else:
                thisClassifier.append('#')
        return thisClassifier
