# -*-coding:Latin-1 -*

import re
import numpy as np

from logPrint import logPrint


class descriptionParser():

    def __init__(self, descriptionList):
        # list is the only accepted type for descriptionList
        self.descriptionLinesList = descriptionList
        self.chaptersMatrix = np.empty((500, 2), dtype=object)

    # Constants
    MAX_SIZE_OF_MATRIX = 100
    MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE = 2

    # self.chaptersMatrixSize

    # Parse the description field to detect the time and title of each chapter
    # Return if it has found chapters
    def parse(self):
        zeroLineFound = self._findLineZero()
        if zeroLineFound:
            # If 0:00 has been found, parse the rest of the chapters
            self._parseChapterList()
        return zeroLineFound

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

    # Returns True if the tested characters seems to not be part of a title name
    def _checkIfCharIsDelimAndNotPartOfTitle(self, char):
        returnValue = (char == "-" or char == " " or char ==
                       "[" or char == "]" or char == "_" or char == "#" or char == ":")
        return returnValue

    # From regex splitting of the line containing 0:00, analyze the pattern to then capture all the chapters in a matrix
    # Patterns description:
    # -1:
    # Not initialized/incorrect
    #
    # 0:
    # "<something_before_or_not><time><title_with_delim_charac>"
    #
    # 1:
    # "<title_with_delim_charac><time>"
    #
    def _analyzeChaptersPattern(self, splittedLineList, idxOfZeroInSplittedLine):
        patternId = -1
        if (idxOfZeroInSplittedLine == 0):
            # The line begins with "0:00"
            patternId = 0
        elif (idxOfZeroInSplittedLine == 1):
            flagAllCharsAreZeroOrColon = True
            # We check if the word before the one detected is part of the time or not
            for char in splittedLineList[0]:
                flagAllCharsAreZeroOrColon = (
                    flagAllCharsAreZeroOrColon and ((char == ':') or (char == '0')))
            if flagAllCharsAreZeroOrColon:
                # The line begins with something like "0:00:00", or less complex
                patternId = 0
            else:
                if (len(splittedLineList[0]) < 3):
                    # The word before is too short to contain the title
                    patternId = 0
                else:
                    # The word before may be the title
                    patternId = 1
        else:
            # Unknown pattern. The script will exit soon later
            patternId = -1
        return patternId

    # Apply regex and double check to look for line containing the chapter 0 at time 0:00
    # Return if it has found chapters
    def _findLineZero(self):
        lineNb = 0
        # Flag to stop the search for 0:00
        isLineAtTimeZero = False

        logPrint.printLog("Parsing the description field")

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
        if not isLineAtTimeZero:
            logPrint.printError("0:00 not found.")

        return isLineAtTimeZero

    # Once the beginning of the chapter list found, parse it entirely and store it in a matrix
    def _parseChapterList(self):
        idxSplitted = 0
        idxOfZeroInSplittedLine = -1
        line = self.descriptionLinesList[self.lineNbZeroZero]
        splittedLineList = re.split(r'([0-9:]+:[0-9:]+)', line)
        for splittedWord in splittedLineList:
            if re.search(r'[0-9:]+:[0-9:]+', splittedWord):
                idxOfZeroInSplittedLine = idxSplitted
            idxSplitted = idxSplitted+1

        # Analyze pattern
        self.patternId = self._analyzeChaptersPattern(
            splittedLineList, idxOfZeroInSplittedLine)
        logPrint.printLog("Pattern detected: "+str(self.patternId))

        idxMatrix = 0
        # To avoid false end-of-chapters due to problems of formatting in the description, another attempt is given to each non-match
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
                if re.search('[0-9:]+:[0-9:]+', line):
                    # Reset for the next formatting error found
                    numberOfRemainingAttemptsToParseEachLine = self.MAX_ATTEMPTS_NB_TO_PARSE_TIME_AND_TITLE

                    # FIXME Does not work for "[2:20] the past inside the present"
                    splittedLine = re.split(r'([0-9:]+:[0-9:]+)', line)

                    # Too specific, commented and will be deleted after testing
                    # offsetForSplittedLineReading = 0
                    # if splittedLine[0] == "":
                    #     # re.split created an empty cell at the beginning, ignore it
                    #     offsetForSplittedLineReading = 1

                    # Pattern 0 could include the case where time is not the first word, the shift to do is idxOfZeroInSplittedLine
                    # We here take thy hypothesis that the shift of the 0:00 line is the same for every line
                    if self.patternId == 0:
                        time = splittedLine[0 + idxOfZeroInSplittedLine]
                        titleAndDelim = splittedLine[1 +
                                                     idxOfZeroInSplittedLine]
                    elif self.patternId == 1:
                        time = splittedLine[1]
                        titleAndDelim = splittedLine[0]
                    else:
                        logPrint.printError(
                            "Chapters pattern not found. Exiting.")
                        exit(-4)

                    logPrint.printLog("Matching line found, line "+str(self.lineNbZeroZero +
                                                                       idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors)+", time "+time)

                    # The flag are used to stop the search when the true beginning/end of the title have been found
                    flagTrueBeginningOfTitleFound = False
                    flagTrueEndOfTitleFound = False
                    # Search for useless characters in the beginning of titleAndDelim that have to be cut
                    # This search is done at the beginning and at the end
                    for idxChar in range(len(titleAndDelim)):
                        # Testing that the chars beginning titleAndDelim are delimiter chars or title letters
                        if not flagTrueBeginningOfTitleFound:
                            isBeginningCharDelimChar = self._checkIfCharIsDelimAndNotPartOfTitle(
                                titleAndDelim[idxChar])
                            if(not isBeginningCharDelimChar):
                                flagTrueBeginningOfTitleFound = True
                                # titleAndDelim[idxChar] is the beginning of the title, we store the index for latter splitting of titleAndDelim
                                idxCharTrueBeginningOfTitle = idxChar

                        # Testing that the chars beginning titleAndDelim are delimiter chars or title letters
                        idxCharReverse = (len(titleAndDelim)-1) - idxChar
                        if not flagTrueEndOfTitleFound:
                            isEndingCharDelimChar = self._checkIfCharIsDelimAndNotPartOfTitle(
                                titleAndDelim[idxCharReverse])
                            if(not isEndingCharDelimChar):
                                flagTrueEndOfTitleFound = True
                                # titleAndDelim[idxChar] is the end of the title, we store the index for latter splitting of titleAndDelim
                                idxCharTrueEndOfTitle = idxCharReverse

                    # The title is splitted to not store useless characters in the beginning
                    # The +1 is here to include the latest detect char of the title
                    title = titleAndDelim[idxCharTrueBeginningOfTitle:idxCharTrueEndOfTitle+1]

                    self.chaptersMatrix[idxMatrix, 0] = time
                    self.chaptersMatrix[idxMatrix, 1] = title

                    # Shift the index only if we have found something to avoid holes because of formatting errors
                    idxMatrix = idxMatrix+1
                else:
                    if numberOfRemainingAttemptsToParseEachLine > 0:
                        # Second chance
                        logPrint.printLog("Not matching line found, line "+str(self.lineNbZeroZero +
                                                                               idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors)+", another chance is given.")
                        numberOfRemainingAttemptsToParseEachLine = numberOfRemainingAttemptsToParseEachLine - 1
                        offsetForIdxMatrixBecauseOfFalseErrors = offsetForIdxMatrixBecauseOfFalseErrors + 1
            else:
                # No more time is detected and the formatting error margin is consumed, the chapter list is over
                logPrint.printLog("No more matching line found, line "+str(self.lineNbZeroZero +
                                                                           idxMatrix + offsetForIdxMatrixBecauseOfFalseErrors)+", the chapter list parsing is over.")
                self.chaptersMatrixSize = idxMatrix
                # End the while loop
                idxMatrix = self.MAX_SIZE_OF_MATRIX

        logPrint.printDebug("chaptersMatrix, " +
                            str(self.chaptersMatrixSize)+" lines: ")
        for idxMatrix in range(self.chaptersMatrixSize):
            logPrint.printDebug("|" +
                                self.chaptersMatrix[idxMatrix, 0]+"|"+self.chaptersMatrix[idxMatrix, 1]+"|")
