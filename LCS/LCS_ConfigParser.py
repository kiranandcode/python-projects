from LCS_Constants import global_constants
import os

class ConfigParser:
    """
        Utility class to set global constants from a configuration file
    """
    def __init__(self, filename):
        self.commentChar = '#'
        self.paramChar = '='
        self.parameters = self.parseConfig(filename)
        global_constants.setConstants(this.parameters)

    def parseConfig(self, filename):
        parameters = {}

        with open(filename) as f:
            for line in f:
                if self.commentChar in line:
                    line, comment = line.split(self.commentChar, 1)

                if self.paramChar in line:
                    parameter, value = line.split(self.paramChar, 1)
                    parameter = parameter.strip()
                    value = value.strip()
                    parameters[parameter] = value

        return parameters
