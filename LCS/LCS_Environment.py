from LCS_DataManager import DataManager
from LCS_Constants import global_constants
import sys


class Environment:
    def __init__(self):
        self.dataRef = 0
        self.storeDataRef = 0
        self.formatData = DataManager(global_constants.trainFile, global_constants.testFile)

        self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
        self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        if global_constants.testFile == 'None':
            pass
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]

    def getTrainInstance(self):
        return [self.currentTrainState, self.currentTrainPhenotype]
    
    def getTestInstance(self):
        return [self.currentTestState, self.currentTestPhenotype]

    def newInstance(self, isTraining):
        if isTraining:
            if self.dataRef < self.formatData.numTrainInstances - 1:
                self.dataRef += 1
                self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
                self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
            else:
                self.resetDataRef(isTraining)
        else:
            if self.dataRef < (self.formatData.numTestInstances-1):
                self.dataRef += 1
                self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
                self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]
    
    def resetDataRef(self, isTraining):
        self.dataRef = 0
        if isTraining:
            self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
            self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]

    def startEvaluationMode(self):
        self.storeDataRef = self.dataRef

    def stopEvaluationMode(self):
        self.dataRef = self.storeDataRef
