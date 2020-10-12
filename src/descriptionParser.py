from logPrint import logPrint


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
                if idxReturnedFromFind > 0:
                    # Check if idxReturnedFromFind>0, if it is really 00:00 and not for example 10:00
                    isLineAtTimeZero = self._checkIfDetectedZeroIsReallyZero(
                        line, idxReturnedFromFind)
                self.idxZeroZero = idxReturnedFromFind
                self.lineNbZeroZero = lineNb
            lineNb = lineNb+1

        # tmp
        logPrint.printDebug("lineNbZeroZero: "+str(self.lineNbZeroZero))

    def _checkIfCharIsBetweenOneAndNine(self, char):
        if char >= '1' and char <= '9':
            return True
        else:
            return False

    def _checkIfDetectedZeroIsReallyZero(self, lineString, idxOfLine):
        logPrint.printDebug(
            "_checkIfDetectedZeroIsReallyZero: #"+str(idxOfLine)+": "+str(lineString[idxOfLine]))
        # Check of underflow
        if (idxOfLine != 0):
            if (self._checkIfCharIsBetweenOneAndNine(lineString[idxOfLine])):
                # No need to go before, the time is bigger than 0:00 (e.g. 20:00)
                returnValue = False
            elif ((lineString[idxOfLine] == '0') or (lineString[idxOfLine] == ':')):
                # There is a 0 before 0:00, go to check before
                returnValue = self._checkIfDetectedZeroIsReallyZero(
                    lineString, idxOfLine-1)
            else:
                # All characters checked from here were 0 or :
                # The one read here is not part of the time
                # We can say for sure the time detected is 0:00
                returnValue = True
        # Beginning of the line
        else:
            if (self._checkIfCharIsBetweenOneAndNine(lineString[idxOfLine])):
                # No need to go before, the time is bigger than 0:00 (e.g. 20:00)
                returnValue = False
            elif ((lineString[idxOfLine] == '0') or (lineString[idxOfLine] == ':')):
                # The time is 0:00 and there is not character left
                returnValue = True
            else:
                # All characters checked from here were 0 or :
                # The one read here is not part of the time
                # We can say for sure the time detected is 0:00
                returnValue = True

        return returnValue
