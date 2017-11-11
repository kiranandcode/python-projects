from LCS_Constants import global_constants
import random
import sys


class DataManager:
    def __init__(self, trainFile, testFile):
        if global_constants.useSeed:
            random.seed(global_constants.randomSeed)
        else:
            random.seed(None)


        self.numAttributes = None      # number of attributes in input file
        self.areInstanceIDs = False    # whether the dataset has a column of instance ids
        self.instanceIDRef = None      # which column is the id column
        self.phenotypeRef = None       # which column specifies the class/phenotype
        self.discretePhenotype = True  # is the class discreet
        self.attributeInfo = []        # stores whether each attribute is discreet or continous
        self.phenotypeList = []        # stores all possible discreet states or minimum max values for continous
        self.phenotypeRange = None     # stores the difference between the min and max for a continous phenotype


        self.trainHeaderList = []
        self.testHeaderList = []
        self.numTrainInstances = []
        self.numTestInstances = []

        rawTrainData = self.loadData(trainFile, True)

        self.characterizeDataset(rawTrainData)

        if testFile == 'None':
            data4Formatting = rawTrainData
        else:
            rawTestData = self.loadData(testFile, False)
            self.compareDataset(rawTestData)
            data4Formatting = rawTrainData + rawTestData

        self.discriminatePhenotype(data4Formatting)
        if self.discretePhenotype:
            self.discriminateClasses(data4Formatting)
        else:
            self.characterizePhenotype(data4Formatting)


        self.discriminateAttributes(data4Formatting)
        self.characterizeAttributes(data4Formatting)


        if testFile != 'None':
            self.testFormatted = self.formatData(rawTestData)

        self.trainFormatted = self.formatData(rawTrainData)


    def loadData(self, dataFile, doTrain):
        datasetList = []
        with open(dataFile,'r') as f:
            if doTrain:
                self.trainHeaderList = f.readline().rstrip('\n').split('\t')
            else:
                self.testHeaderList = f.readline().rstrip('\n').split('\t')

            for line in f:
                lineList = line.strip('\n').split('\t')
                datasetList.append(lineList)
        return datasetList
    

    def characterizeDataset(self, rawTrainData):
        if global_constants.labelInstanceID in self.trainHeaderList:
            self.areInstanceIDs = True
            self.instanceIDRef = self.trainHeaderList.index(global_constants.labelInstanceID)
            self.numAttributes = len(self.trainHeaderList) - 2 # 1 for id and 1 for phenotype
        else:
            self.numAttributes = len(self.trainHeaderList) - 1

        if global_constants.labelPhenotype in self.trainHeaderList:
            self.phenotypeRef = self.trainHeaderList.index(global_constants.labelPhenotype)
        else:
            raise ValueError('Could not find phenotype ref {} in header list'.format(global_constants.labelPhenotype))

        # only include attributes in dataset
        if self.areInstanceIDs:
            if self.phenotypeRef > self.instanceIDRef:
                self.trainHeaderList.pop(self.phenotypeRef)
                self.trainHeaderList.pop(self.instanceIDRef)
            else:
                self.trainHeaderList.pop(self.instanceIDRef)
                self.trainHeaderList.pop(self.phenotypeRef)
        else:
            self.trainHeaderList.pop(self.phenotypeRef)

    def discriminatePhenotype(self, rawData):
        inst = 0
        classDict = {}
        while self.discretePhenotype and len(list(classDict.keys())) <= global_constants.discreteAttributeLimit and inst < self.numTrainInstances:
            target = rawData[inst][self.phenotypeRef]
            if target in list(classDict.keys()):
                classDict[target] += 1
            elif target ==  global_constants.labelMissingData:
                pass
            else:
                classDict[target] = 1

        if len(classDict.keys()) > global_constants.discreteAttributeLimit:
            self.discretePhenotype = False
            self.phenotypeList = [float(target), float(target)]

    def discriminateClasses(self, rawData):
        inst = 0
        classCount = {}
        while inst < self.numTrainInstances:
            target = rawData[inst][self.phenotypeRef]
            if target in self.phenotypeList:
                classCount.setdefault(target, classCount.get(target, 0) + 1)
            inst += 1
        for each in classCount.keys():
            print("Class: " + str(each) + " count = " + str(classCount[each]))

    def compareDataset(self, rawTestData):
        if self.areInstanceIDs:
            if self.phenotypeRef > self.instanceIDRef:
                self.testHeaderList.pop(self.phenotypeRef)
                self.testHeaderList.pop(self.instanceIDRef)
            else:
                self.testHeaderList.pop(self.instanceIDRef)
                self.testHeaderList.pop(self.phenotypeRef)
        else:
            self.testHeaderList.pop(self.phenotypeRef)

        if self.trainHeaderList != self.testHeaderList:
            raise ValueError('Testing and training data headers do not match')

        self.numTestInstances = len(rawTestData)
    
    def discriminateAttributes(self, rawData):
        self.discreteCount = 0
        self.continousCount = 0
        for attr in range(len(rawData[0])):
            if attr != self.instanceIDRef and attr != self.phenotypeRef:
                attrIsDiscrete = True
                inst = 0
                stateDict = {}
                while attrIsDiscrete and len(stateDict.keys()) <= global_constants.discreteAttributeLimit and inst < self.numTrainInstances:
                    target = rawData[inst][attr]
                    if target == global_constants.labelMissingData:
                        pass
                    elif target in stateDict.keys():
                        stateDict[target] += 1
                    else:
                        stateDict[target] = 1
                    inst += 1
                if len(stateDict.keys()) > global_constants.discreteAttributeLimit:
                    attrIsDiscrete = False
                
                if attrIsDiscrete:
                    self.attributeInfo.append([0,[]])
                    self.discreteCount += 1
                else:
                    self.attributeInfo.append([1,[float(target), float(target)]])
                    self.continousCount += 1


    def characterizeAttributes(self, rawData):
        attributeId = 0
        for attr in range(len(rawData[0])):
            if attr != self.instanceIDRef and attr != self.phenotypeRef:
                for inst in range(len(rawData)):
                    target[inst][attr]

                    if not self.attributeInfo[attributeId][0]:
                        if target in self.attributeInfo[attributeId][1] or target == global_constants.labelMissingData:
                            pass
                        else:
                            self.attributeInfo[attributeId][1].append(target)
                    else:

                        if target == cons.labelMissingData:
                            pass
                        elif float(target) > self.attributeInfo[attributeId][1][1]:
                            self.attributeInfo[attributeId][1][1] = float(target)
                        elif float(target) < self.attributeInfo[attributeId][1][0]:
                            self.attributeInfo[attributeId][1][0] - float(target)
                        else:
                            pass
                attributeId += 1

    def characterizePhenotype(self, rawData):
        for inst in range(len(rawData)):
            target = rawData[inst][self.phenotypeRef]

            if target == global_constants.labelMissingData:
                pass
            elif float(target) > self.phenotypeList[1]:
                self.phenotypeList[1] = float(target)
            elif float(target) < self.phenotypeList[0]:
                self.phenotypeList[0] = float(target)
            else pass
        self.phenotypeRange = self.phenotypeList[1] - self.phenotypeList[0]
    

    def formatData(self, rawData):

        formatted = []

        for i in range(len(rawData)):
            formatted.append([None, None, None])

        for inst in range(len(rawData)):
            stateList = []
            attributeId = 0
            for attr in range(len(rawData[0])):
                if attr != self.instanceIDRef and attr != self.phenotypeRef:
                    target = rawData[inst][attr]

                    if self.attributeInfo[attributeId][0]:
                        if target == cons.labelMissingData:
                            stateList.append(target)
                        else:
                            stateList.append(float(target))
                    else:
                        stateList.append(target)
                    attributeId += 1

            formatted[inst][0] = stateList
            if self.discretePhenotype:
                formatted[inst][1] = rawData[inst][self.phenotypeRef]
            else:
                formatted[inst][1] = float(rawData[inst][self.phenotypeRef])
            if self.areInstanceIDs:
                formatted[inst][2] = rawData[inst][self.instanceIDRef]
        
        random.shuffle(formatted)
        return formatted
