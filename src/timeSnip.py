# -*-coding:Latin-1 -*

import sys

from logPrint import logPrint
from youtubeApiWrapper import youtubeApiWrapper
from descriptionParser import descriptionParser
from musicDisplayer import musicDisplayer


def main(argv):
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
        # returns a line of str
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

    # FIXME to get from a .ini file, not as a main arg
    outputFilePath = "D:\\Program Files\\Snip\\Snip.txt"

    # Instantiate musicDisplayer to launch a timer and print the correct music name
    musicDisplayerInst = musicDisplayer(outputFilePath, chaptersMatrix)

    # Launch the timer
    musicDisplayerInst.start()


if __name__ == "__main__":
    # Log level = debug
    logPrint(0)

    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        logPrint.printError("Usage: timeSnip <YoutubeURL>")
        exit(-1)
