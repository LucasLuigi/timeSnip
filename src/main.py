# -*-coding:Latin-1 -*

import sys
from musicTimer import *
from logPrint import *
from youtubeApiWrapper import *


def main(argv):
    # Log level = debug
    logPrint(0)

    youtubeApiInst = youtubeApiWrapper(sys.argv[1])
    youtubeApiInst.getDescriptionField()
    # threadMusicTimer = musicTimer()
    # threadMusicTimer.start()
    # threadMusicTimer.join()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        print("Usage: timeSnip <YoutubeURL>")
        exit(-1)
