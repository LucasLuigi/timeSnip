# -*-coding:Latin-1 -*

from musicTimer import *
from logPrint import *


def main():
    # Log level = debug
    logPrint(0)
    threadMusicTimer = musicTimer()
    threadMusicTimer.start()
    threadMusicTimer.join()


if __name__ == "__main__":
    main()
