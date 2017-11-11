
class Constants:
    """
    Retrieves constants from a config file and provides in code access
    """
    def setConstants(self, par):
        self.trainFile = par['trainFile']
        self.testFile = par['testFile']
        self.outFile = par['outFileName'] 
        self.learningIterations = par['learningIterations']
        self.N = int(par['N'])

        if par['randomSeed'].lower() == 'false':
            self.useSeed = False
        elif par['randomSeed'].lower() == 'true':
            self.useSeed = True
            self.randomSeed = int(par['randomSeed'])
        else:
            raise ValueError('{} is not a valid option for randomSeed'.format(par['randomSeed'])

        self.labelInstanceID = par['labelInstanceID']
        self.labelPhenotype = par['labelPhenotype']
        self.labelMissingData = par['labelMissingData']
        self.discreteAttributeLimit = int(par['discreetAttributeLimit'])

        self.init_fit = float(par['init_fit'])
        self.p_spec = float(par['p_spec'])
        self.nu = float(par['nu'])


global_constants = Constants()
