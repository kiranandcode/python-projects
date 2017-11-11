from LCS_Constants import global_constants
from LCS_ClassifierSet import ClassifierSet
import copy
import random
import math

class LCS:
    def __init__(self):

        self.population = None
        self.learnTrackOut = None

        if global_constants.doPopulationReboot:
            self.populationReboot()
        else:
            self.learnTrackOut = open(global_constants.outFile, 'w')

            self.population = ClassifierSet()
            self.exploreIter = 0
            self.correct = [0.0 for i in range(global_constants.trackingFrequency)]

        self.run_LCS()

    def run_LCS(self):
        while self.exploreIter < global_constants.maxLearningIterations:
            
            state_phenotype = global_constants.env.getTrainInstance()
            self.runIteration(state_phenotype, self.exploreIter)

            if self.exploreIter % global_constants.trackingFrequency == global_constants.trackingFrequency - 1:
                self.population.runPopAveEval(self.exploreIter)
                self.learnTrackOut.write(self.population.getPopTrack(self.exploreIter+1, global_constants.trackingFrequency))

            self.exploreIter += 1
            global_constants.env.newInstance(True)
        self.learnTrackOut.close()

    def runIteration(self, state_phenotype, exploreIter):

        self.population.makeMatchSet(state_phenotype, exploreIter)
        self.population.makeCorrectSet(state_phenotype[1])
        self.population.updateSets(exploreIter)
        self.population.clearSets()

    def populationReboot(self):
        self.learnTrackOut = open(global_constants.outFile,'a')
        temp = global_constants.populationRebootPath.split('_')
        iterRef = len(temp)-1
        self.exploreIter = completedIterations-1
        for i in range(len(global_constants.learningCheckpoints):
            global_constants.learningCheckpoints[i] += completedIterations
        global_constants.maxLearningIterations += completedIterations
        self.population = ClassifierSet(global_constants.populationRebootPath)

