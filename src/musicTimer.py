# -*-coding:Latin-1 -*

from threading import Thread
import time


class musicTimer(Thread):

    def __init__(self):
        Thread.__init__(self)
        # self.lettre = lettre
        print("a")

    def run(self):
        i = 0
        while i < 20:
            i += 1
            print(i)