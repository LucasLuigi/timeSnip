# -*-coding:Latin-1 -*

import time
import numpy as np

from logPrint import logPrint


class musicDisplayer():

    def __init__(self, filePath, chaptersMatrix, prefix):
        self.chaptersMatrix = chaptersMatrix
        self.filePath = filePath
        self.prefix = prefix
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

            self._writeTitleInFile(self.prefix+nextTitle)

            # Store the date for the next iteration
            previousDate = nextDate

        # FIXME Wait for the end of the last song (we do not have the info) before flushing the file
        logPrint.printInfo("End of the video, erasing the file")
        # self._writeTitleInFile("")

    def _writeTitleInFile(self, title):
        if len(title) > 0:
            logPrint.printInfo("Writing \""+title+"\"")

        f = open(self.filePath, "w", encoding="utf-8")
        f.write(title)
        f.close()
