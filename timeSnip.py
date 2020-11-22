# -*-coding:Latin-1 -*

import sys

from internalConfig import internalConfig
from logPrint import logPrint
from youtubeApiWrapper import youtubeApiWrapper
from descriptionParser import descriptionParser
from musicDisplayer import musicDisplayer


def main(outputFilePath, argv):
    prefix = ""

    youtubeApiInst = youtubeApiWrapper(sys.argv[1])
    descrFromYoutubeApi = youtubeApiInst.getDescriptionField()
    # descriptionParser acceptis only list of str
    descrListFromYoutubeApi = descrFromYoutubeApi.splitlines()

    # First attempt of chapter parsing using what Youtube API returned
    descriptionParserInstFromYoutube = descriptionParser(
        descrListFromYoutubeApi)
    succesfullParsing = descriptionParserInstFromYoutube.parse()
    if(not succesfullParsing):
        logPrint.printInfo(
            "Another attempt can be given using pasted chapter list.")
        # Another parsing is attempted using stdin
        logPrint.printInfo(
            "Copy/paste the description list you want, then hit Ctrl+Z")
        # returns a list of str
        descrListFromCopyPaste = sys.stdin.readlines()
        # strip this line from "\n"
        strippedDescrListFromCopyPaste = [
            "" for idx in range(len(descrListFromCopyPaste))]
        for idx in range(len(descrListFromCopyPaste)):
            strippedDescrListFromCopyPaste[idx] = descrListFromCopyPaste[idx].strip(
                " \n")
        # Create a new descriptionParser with the pasted list stripped from the final \n
        descriptionParserInstFromCopyPaste = descriptionParser(
            strippedDescrListFromCopyPaste)
        succesfullParsing = descriptionParserInstFromCopyPaste.parse()
        if(not succesfullParsing):
            logPrint.printError("Second attempt failed. Exiting.")
            exit(-5)
        else:
            chaptersMatrix = descriptionParserInstFromCopyPaste.getChaptersMatrix()
    else:
        chaptersMatrix = descriptionParserInstFromYoutube.getChaptersMatrix()

    if len(sys.argv) == 3:
        prefix = sys.argv[2]
        logPrint.printLog("The prefix \""+prefix +
                          "\" read from the program's arguments, will be added before each title.")
    else:
        prefix = ""
        logPrint.printLog("No prefix read from the program's arguments.")

    # Instantiate musicDisplayer to launch a timer and print the correct music name
    musicDisplayerInst = musicDisplayer(outputFilePath, chaptersMatrix, prefix)

    # Launch the timer
    musicDisplayerInst.start()


if __name__ == "__main__":
    # Parsing config.ini
    internalConfigInst = internalConfig()

    logLevel = internalConfigInst.getVerbosityLevel()
    outputFilePath = internalConfigInst.getOutputFilePath()

    # Log level = debug
    logPrint(logLevel)

    logPrint.printDebug("Config.ini: logLevel="+str(logLevel))
    logPrint.printDebug("Config.ini: outputFilePath="+outputFilePath)

    if len(sys.argv) >= 2 and len(sys.argv) <= 3:
        main(outputFilePath, sys.argv[1:])
    else:
        logPrint.printError("Usage: timeSnip.py <YoutubeURL> [prefix]")
        exit(-1)
