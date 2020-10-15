# -*-coding:Latin-1 -*

import re
import numpy as np

from logPrint import logPrint


class descriptionParser():

    def __init__(self, description):
        self.description = description
        self.chaptersMatrix = np.empty((500, 2), dtype=object)

    # Constants
    MAX_SIZE_OF_MATRIX = 500
    MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE = 2

    # self.chaptersMatrixSize

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
                flagAllCharsAreZeroOrColonOrSpace = (flagAllCharsAreZeroOrColonOrSpace and ((
                    char == ' ') or (char == ':') or (char == '0')))
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
            logPrint.printError("0:00 not found. Exiting.")
            exit(-3)

    # Once the beginning of the chapter list found, parse it entirely and store it in a matrix
    def _parseChapterList(self):
        idxSplitted = 0
        idxOfZeroInSplittedLine = -1
        line = self.descriptionLinesList[self.lineNbZeroZero]
        splittedLineList = re.split(r'([0-9]:[0-9][0-9])', line)
        for splittedWord in splittedLineList:
            if re.search('[0-9]:[0-9][0-9]', splittedWord):
                idxOfZeroInSplittedLine = idxSplitted
            idxSplitted = idxSplitted+1

        # Analyze pattern
        self.patternId = self._analyzeChaptersPattern(
            splittedLineList, idxOfZeroInSplittedLine)
        logPrint.printLog("Pattern detected: "+str(self.patternId))

        idxMatrix = 0
        # To avoid false end of chapters due to problems of formatting in the description, another attempt is given to each non-match
        numberOfRemainingAttemptsToParseEachLine = self.MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE
        logPrint.printLog("While parsing the chapters, a maximum of "+str(
            self.MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE)+" not matching line(s) is accepted.")
        offsetForIdxMatrixBecauseOfFalseErrors = 0

        # Max length of the matrix
        while (idxMatrix < self.MAX_SIZE_OF_MATRIX):
            # Avoid overflow
            if((self.lineNbZeroZero + idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors < len(self.descriptionLinesList)) and numberOfRemainingAttemptsToParseEachLine > 0):
                line = self.descriptionLinesList[self.lineNbZeroZero +
                                                 idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors]
                if re.search('[0-9]:[0-5][0-9]', line):
                    # Reset for the next formatting error found
                    numberOfRemainingAttemptsToParseEachLine = self.MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE

                    splittedLine = re.split(r'([0-9:]+)', line)
                    # FIXME not robust
                    offsetForSplittedLineReading = 0
                    if splittedLine[0] == "":
                        # re.split created an empty cell at the beginning, ignore it
                        offsetForSplittedLineReading = 1
                    if self.patternId == 0:
                        time = splittedLine[0 + offsetForSplittedLineReading]
                        title = splittedLine[1 + offsetForSplittedLineReading]
                    elif self.patternId == 1:
                        time = splittedLine[1 + offsetForSplittedLineReading]
                        title = splittedLine[0 + offsetForSplittedLineReading]
                    else:
                        logPrint.printError(
                            "Chapters pattern not found. Exiting.")
                        exit(-4)
                    self.chaptersMatrix[idxMatrix, 0] = time
                    self.chaptersMatrix[idxMatrix, 1] = title

                    # Shift the index only if we have found something to avoid holes because of formatting errors
                    idxMatrix = idxMatrix+1
                else:
                    if numberOfRemainingAttemptsToParseEachLine > 0:
                        # Second chance
                        numberOfRemainingAttemptsToParseEachLine = numberOfRemainingAttemptsToParseEachLine - 1
                        offsetForIdxMatrixBecauseOfFalseErrors = offsetForIdxMatrixBecauseOfFalseErrors + 1
                        logPrint.printLog("Not matching line found line "+str(self.lineNbZeroZero +
                                                                              idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors)+", another chance is given.")
            else:
                # No more time is detected and the formatting error margin is consumed, the chapter list is over
                self.chaptersMatrixSize = idxMatrix
                # End the while loop
                idxMatrix = self.MAX_SIZE_OF_MATRIX

        logPrint.printLog("The chapter matrix is " +
                          str(self.chaptersMatrixSize)+" lines long.")
