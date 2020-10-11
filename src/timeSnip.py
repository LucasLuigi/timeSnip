# -*-coding:Latin-1 -*

import sys

from logPrint import logPrint
from youtubeApiWrapper import youtubeApiWrapper
from descriptionParser import descriptionParser


def main(argv):
    youtubeApiInst = youtubeApiWrapper(sys.argv[1])
    description = youtubeApiInst.getDescriptionField()

    descriptionParserInst = descriptionParser(description)
    descriptionParserInst.parse()

    # threadMusicTimer = musicTimer()
    # threadMusicTimer.start()
    # threadMusicTimer.join()


if __name__ == "__main__":
    # Log level = debug
    logPrint(0)

    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        logPrint.printError("Usage: timeSnip <YoutubeURL>")
        exit(-1)
