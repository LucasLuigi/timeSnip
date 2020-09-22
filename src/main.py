# -*-coding:Latin-1 -*

from musicTimer import musicTimer


if __name__ == "__main__":
    print("Hello world")
    threadMusicTimer = musicTimer()
    threadMusicTimer.start()
    threadMusicTimer.join()
