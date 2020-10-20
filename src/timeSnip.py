# -*-coding:Latin-1 -*

import sys

from logPrint import logPrint
from youtubeApiWrapper import youtubeApiWrapper
from descriptionParser import descriptionParser


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
                "\n")
        # Create a new descriptionParser with the pasted list stripped from the final \n
        descriptionParserInstFromCopyPaste = descriptionParser(
            strippedDescrListFromCopyPaste)
        succesfullParsing = descriptionParserInstFromCopyPaste.parse()
        if(not succesfullParsing):
            logPrint.printError("Second attempt failed. Exiting.")
            exit(-5)


if __name__ == "__main__":
    # Log level = debug
    logPrint(0)

    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        logPrint.printError("Usage: timeSnip <YoutubeURL>")
        exit(-1)
