'''
    Created by Eric
    on Apr.20.2020

    The main program run on server
'''

from config_file import *
from switch import Switch

class Main:
    def __init__(self):
        self.VS = Switch(IP, VIDEO_IN_PORT, VIDEO_OUT_PORT, 4096)
        self.DS = Switch(IP, DATA_IN_PORT, DATA_OUT_PORT, 1024)
        self.CS = Switch(IP, CMD_IN_PORT, CMD_OUT_PORT, 1024)

    def run(self):
        self.VS.run()
        self.DS.run()
        self.CS.run()

if __name__ == "__main__":
    M = Main()
    M.run()