from logPrint import *


class descriptionParser():

    def __init__(self, description):
        self.description = description

    def parse(self):
        lineNb = 0

        logPrint.printLog("Parsing the description field")
        self.descriptionLinesList = self.description.splitlines()
        for line in self.descriptionLinesList:
            idxReturnedFromFind = line.find("0:00")
            if idxReturnedFromFind != -1:
                # "0:00" found. We store the line number and the character index
                # TODO Check if idxReturnedFromFind>0, if it is really 00:00 and not for example 10:00
                self.idxZeroZero = idxReturnedFromFind
                self.lineNbZeroZero = lineNb
            lineNb = lineNb+1

        # tmp
        logPrint.printDebug("lineNbZeroZero: "+str(self.lineNbZeroZero))
