from LCS_Constants import global_constants
from LCS_Classifier import Classifier
import random
import copy
import sys


class ClassifierSet:
    def __init__(self, a=None):
        self.popSet = []
        self.matchSet = []
        self.correctSet = []
        self.microPopSize = 0

        self.aveGenerality = 0.0
        self.expRules = 0.0
        self.attributeSpecList = []
        self.attributeAccList = []
        self.avePhenotypeRange = 0.0

        if a == None:
            self.makePop()
        elif isinstance(a,str):
            self.rebootPop(a)
        else:
            raise ValueError("Invalid parameters to construct a Classifier set")
    
    def makePop(self):
        self.popSet = []
    
    def rebootPop(self, remakeFile):

        with open(remakeFile,'r') as f:
            self.headerList = f.readLine().rstrip('\n').split('\t')
            for line in f:
                lineList = line.strip('\n').split('\t')
                datasetList.append(lineList)

        for each in datasetList:
            cl = Classifier(each)
            self.popSet.append(cl)
            self.microPopSize += 1

    def makeMatchSet(self, state_phenotype, exploreIter):
        state = state_phenotype[0]
        phenotype = state_phenotype[1]
        doCovering = True


        for i in range(len(self.popSet)):
            cl = self.popSet[i]
            if cl.match(state):

                self.matchSet.append(i)
                if global_constants.env.formatData.discretePhenotype:
                    if cl.phenotype == phenotype:
                        doCovering = False
                else:
                    if float(cl.phenotype[0]) <= float(phenotype) <= float(cl.phenotype[1]):
                            doCovering = False
        if len(self.matchSet) == 0:
            print('No matches found')

        while doCovering:
            newCl = Classifier(exploreIter, state, phenotype)

            self.addClassifierToPopulation(newCl)
            self.matchSet.append(len(self.popSet)-1)
            doCovering = False

    def makeCorrectSet(self, phenotype):
        for i in range(len(self.matchSet)):
        ref = self.matchSet[i]

        if global_constants.env.formatData.discretePhenotype:
            if self.popSet[ref].phenotype == phenotype:
                self.correctSet.append(ref)
        else:
            if float(phenotype) <= float(self.popSet[ref].phenotype[1]) and float(phenotype) >= float(self.popSet[ref].phenotype[0]):
                self.correctSet.append(ref)
    
    def addClassifierToPopulation(self, cl):
        self.popSet.append(cl)
        self.microPopSize += 1


    def updateSets(self, exploreIter):

        for ref in self.matchSet:
            self.popSet[ref].updateExperience()
            if ref in self.correctSet:
                self.popSet[ref].updateCorrect
            self.popSet[ref].updateAccuracy()
            self.popSet[ref].updateFitness()


    def setIterStamps(self, exploreIter):
        for i in range(len(self.correctSet)):
            ref = self.correctSet[i]
            self.popSet[ref].updateTimeStamp(exploreIter)

    def clearSets(self):
        self.matchSet = []
        self.popSet = []

    def runPopAveEval(self, exploreIter):
        genSum = 0
        agedCount = 0
        for cl in self.popSet:
            genSum += ((global_constants.env.formatData.numAttributes - len(cl.condition))/float(global_constants.env.formatData.numAttributes))
        if self.microPopSize == 0:
            self.aveGenerality = 'NA'
        else:
            self.aveGenerality = genSum / float(self.microPopSize)

        if not global_constants.env.formatData.discretePhenotype:
            sumRuleRange = 0
            for cl in self.popSet:
                sumRuleRange += (cl.phenotype[1] - cl.phenotype[0])
            phenotypeRange = global_constants.env.formatData.phenotypeList[1] - global_constants.env.formatData.phenotypeList[0]
            self.avePhenotypeRange = (sumRuleRange/float(self.microPopSize))/ float(phenotypeRange)

    def getPopTrack(self, exploreIter, trackingFrequency):
        trackString = str(exploreIter) + "\t" + str(len(self.popSet)) + "\t" + str(self.aveGenerality) + "\n"
        return trackString


