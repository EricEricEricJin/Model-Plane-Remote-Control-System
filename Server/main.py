'''
    Created by Eric
    on Apr.20.2020

    The main program run on server
'''

from switch import Switch

IP = "127.0.0.1"

VIDEO_IN_PORT = 2000
VIDEO_OUT_PORT = 2400
VIDEO_HBP = 2500

DATA_IN_PORT = 2100
DATA_OUT_PORT = 2600
DATA_HBP = 2700

CMD_IN_PORT = 2800
CMD_OUT_PORT = 2200
CMD_HBP = 2300

class Main:
    def __init__(self):
        self.VS = Switch(IP, VIDEO_IN_PORT, VIDEO_OUT_PORT, VIDEO_HBP, 40960)
        self.DS = Switch(IP, DATA_IN_PORT, DATA_OUT_PORT, DATA_HBP, 1024)
        self.CS = Switch(IP, CMD_IN_PORT, CMD_OUT_PORT, CMD_HBP, 1024)

    def run(self):
        self.VS.run()
        self.DS.run()
        self.CS.run()


if __name__ == "__main__":
    M = Main()
    M.run()
