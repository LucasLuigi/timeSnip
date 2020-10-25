# -*-coding:Latin-1 -*

import time
import numpy as np

from logPrint import logPrint


class musicDisplayer():

    def __init__(self, filePath, chaptersMatrix):
        self.chaptersMatrix = chaptersMatrix
        self.filePath = filePath
        logPrint.printInfo("File path is "+self.filePath)

    def start(self):
        logPrint.printInfo("Starting the timer to display the chapters.")

        previousDate = 0
        for idxChapter in range(len(self.chaptersMatrix)):
            nextDate = self.chaptersMatrix[idxChapter, 0]
            nextTitle = self.chaptersMatrix[idxChapter, 1]
            durationBeforeNextTitle = nextDate-previousDate
            # Execution is paused before next milestone
            time.sleep(float(durationBeforeNextTitle))

            self._writeTitleInFile(nextTitle)

            # Store the date for the next iteration
            previousDate = nextDate

    def _writeTitleInFile(self, title):
        logPrint.printInfo("Writing \""+title+"\"")

        f = open(self.filePath, "w", encoding="utf-8")
        # TODO Add customized prefix/suffix (Artist...)
        f.write(title)
        f.close()
