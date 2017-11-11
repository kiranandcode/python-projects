from LCS_ClassifierSet import ClassifierSet
from LCS_Constants import *
import copy
import random
import math


class eLCS:
    def __init__(self):
        self.population = None
        self.learnTrackOut = None

        if cons.doPopulationReboot:
            self.populationReboot()

        else:
            try:
                self.learnTrackOut = open(cons.outFileName + '_LearnTrack.txt', 'w')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', cons.outFileName + '_LearnTrack.txt')
                raise
            else:
                self.learnTrackOut.write("Explore_Iteration\tPopSize\tAveGenerality\n")

            self.population = ClassifierSet()
            self.exploreIter = 0
            self.correct = [0.0 for i in range(cons.trackingFrequency)]


        self.run_LCS()

    def run_LCS(self):
        print("Learning Checkpoints: " + str(cons.learningCheckpoints))
        print("Maximum Iterations: " + str(cons.maxLearningIterations))
        print("Beginning eLCS Learning iterations.")


        while self.exploreIter < cons.maxLearningIterations:

            state_phenotype = cons.env.getTrainInstance()
            self.runIteration(state_phenotype, self.exploreIter)

            if (self.exploreIter%cons.trackingFrequency) == (cons.trackingFrequency - 1):
                self.population.runPopAveEval(self.exploreIter)
                self.learnTrackOut.write(self.population.getPopTrack(self.exploreIter+1, cons.trackingFrequency))

            self.exploreIter += 1
            cons.env.newInstance(True)

        self.learnTrackOut.close()
        print("eLCS run complete")

    def runIteration(self, state_phenotype, exploreIter):

        self.population.makeMatchSet(state_phenotype, exploreIter)

        self.population.makeCorrectSet(state_phenotype[1])

        self.population.updateSets(exploreIter)
        self.population.clearSets()

    def populationReboot(self):

        try:
            self.learnTrackOut = open(cons.outFileName + '_LearnTrack.txt', 'a')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.outFileName + '_LearnTrack.txt')
            raise
        
        temp = cons.popRebootPath.split('_')
        iterRef = len(temp) - 1
        completedIterations = int(temp[iterRef])
        print("Rebooting rule population after " + str(completedIterations) + " iterations")
        
        self.exploreIter = completedIterations - 1
        for i in range(len(cons.learningCheckpoints)):
            cons.learningCheckpoints[i] += completedIterations
        cons.maxLearningIterations += completedIterations
        
        self.population = ClassifierSet(cons.popRebootPath)


