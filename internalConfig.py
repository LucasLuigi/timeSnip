# -*-coding:Latin-1 -*

import configparser
from pathlib import Path

from logPrint import logPrint


class internalConfig():
    # This class will parse the .ini config file

    def __init__(self):
        logPrint.printLog("Parsing the config file config.ini")
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.outputFilePath = self.config['timeSnip']['outputFilePath']
        readVerbosityLevel = self.config['timeSnip']['verbosityLevel']

        # outputFilePath
        if self.outputFilePath == "":
            print(
                "[ERR] In internalConfig.py, outputFilePath is not defined")
            exit(-7)
        outputFile = Path(self.outputFilePath)
        outputFileParent = outputFile.parent
        if not outputFileParent.is_dir():
            print(
                "[ERR] In internalConfig.py, outputFilePath is bad defined: its parent directory does not exist")
            exit(-8)

        # verbosityLevel
        if readVerbosityLevel == "":
            print(
                "[ERR] In internalConfig.py, readVerbosityLevel is not defined")
            exit(-7)
        if readVerbosityLevel == "debug":
            self.verbosityLevel = 0
        elif readVerbosityLevel == "log":
            self.verbosityLevel = 1
        elif readVerbosityLevel == "error":
            self.verbosityLevel = 2
        else:
            print("[ERR] In internalConfig.py, verbosityLevel is not/bad defined")
            exit(-9)

    def getOutputFilePath(self):
        return self.outputFilePath

    def getVerbosityLevel(self):
        return self.verbosityLevel
