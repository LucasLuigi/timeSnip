# -*-coding:Latin-1 -*

import re
import numpy as np

from logPrint import logPrint


class descriptionParser():

    def __init__(self, description):
        self.description = description
        self.chaptersMatrix = np.empty((500, 2), dtype=object)

    # Parse the description field to detect the time and title of each chapter
    def parse(self):
        self._findLineZero()
        self._parseChapterList()

        # tmp
        logPrint.printDebug("lineNbZeroZero: "+str(self.lineNbZeroZero))

    # Check if the character as argument is 1, 2, 3, 4, 5, 6, 7, 8 or 9
    def _checkIfCharIsBetweenOneAndNine(self, char):
        if char >= '1' and char <= '9':
            return True
        else:
            return False

    # Double check if the regex applied to find 0:00 has really found 0:00 and not 10:00 for instance
    # Detect also as a positive 00:00 or 0:00:00 for instance
    def _checkIfDetectedZeroIsReallyZero(self, lineString, idxOfLine):
        # logPrint.printDebug(
        #     "_checkIfDetectedZeroIsReallyZero: #"+str(idxOfLine)+": "+str(lineString[idxOfLine]))

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

    # From regex splitting of the line containing 0:00, analyze the pattern to then capture all the chapters in a matrix
    # Patterns description:
    # -1:
    # Not initialized/incorrect
    #
    # 0:
    # "<time> <title_with_delim_charac>"
    #
    # 0:
    # "<title_with_delim_charac> <time>"
    #
    def _analyzeChaptersPattern(self, splittedLineList, idxOfZeroInSplittedLine):
        patternId = -1
        if (idxOfZeroInSplittedLine == 0):
            # <time> is "0:00"
            patternId = 0
        elif (idxOfZeroInSplittedLine == 1):
            flagAllCharsAreZeroOrColonOrSpace = True
            for char in splittedLineList[0]:
                flagAllCharsAreZeroOrColonOrSpace = (flagAllCharsAreZeroOrColonOrSpace and (
                    char == ' ') and (char == ':') and (char == '0'))
            if flagAllCharsAreZeroOrColonOrSpace:
                # <time> is something like " 0:00:00", or less complex
                patternId = 0
            else:
                patternId = 1
        else:
            patternId = 1
        return patternId

    # Apply regex and double check to look for line containing the chapter 0 at time 0:00
    def _findLineZero(self):
        lineNb = 0
        # Flag to stop the search for 0:00
        isLineAtTimeZero = False

        logPrint.printLog("Parsing the description field")

        self.descriptionLinesList = self.description.splitlines()
        for line in self.descriptionLinesList:
            if (not isLineAtTimeZero):
                # Not find yet: perform the search
                idxReturnedFromFind = line.find("0:00")
                if idxReturnedFromFind != -1:
                    # "0:00" found. We store the line number and the character index
                    if idxReturnedFromFind > 0:
                        # Consolidate: check again if idxReturnedFromFind>0, i.e. if it is really 00:00 and not for example 10:00
                        isLineAtTimeZero = self._checkIfDetectedZeroIsReallyZero(
                            line, idxReturnedFromFind)
                    else:
                        # 0:00 at index 0 is for sure a time zero
                        isLineAtTimeZero = True
                    if isLineAtTimeZero:
                        # self.idxCharZeroZero = idxReturnedFromFind
                        self.lineNbZeroZero = lineNb
                lineNb = lineNb+1
        if (not isLineAtTimeZero):
            logPrint.printError("Error: 0:00 not found. Exiting.")
            exit(-3)

    # Once the beginning of the chapter list found, parse it entirely and store it in a matrix
    def _parseChapterList(self):
        idxSplitted = 0
        idxOfZeroInSplittedLine = -1
        totalLineNb = len(self.descriptionLinesList)
        line = self.descriptionLinesList[self.lineNbZeroZero]
        splittedLineList = re.split(r'([0-9]:[0-9][0-9])', line)
        for splittedWord in splittedLineList:
            if re.search('[0-9]:[0-9][0-9]', splittedWord):
                idxOfZeroInSplittedLine = idxSplitted
            idxSplitted = idxSplitted+1

        # Analyze pattern
        self.patternId = self._analyzeChaptersPattern(
            splittedLineList, idxOfZeroInSplittedLine)

        # FIXME tmp
        idxMatrix = 0
        while (idxMatrix < 4):
            line = self.descriptionLinesList[self.lineNbZeroZero+idxMatrix]
            splittedLine = re.split(r'([0-9:]+)', line)
            if self.patternId == 0:
                time = splittedLine[0]
                title = splittedLine[1]
            elif self.patternId == 1:
                time = splittedLine[1]
                title = splittedLine[0]
            self.chaptersMatrix[idxMatrix, 0] = time
            self.chaptersMatrix[idxMatrix, 1] = title
            idxMatrix = idxMatrix+1

        logPrint.printDebug("patternId: "+str(self.patternId))
