'''
    Created by Eric
    on Apr.11.2020
    
    Class to communicate(send/recv) with server
'''

from communications.receive_cmd import receiveCmd
from communications.send_data import sendData
from communications.send_video import sendVideo

class Communication:
    def __init__(self):
        self.RC = receiveCmd()
        self.SD = sendData()
        self.SV = sendVideo()

    def init(self):
        self.RC.init()
        self.SD.init()
        self.SV.init()

    def run(self):
        self.RC.run()
        self.SD.run()
        self.SV.run()

    def __del__(self):
        del(self.RC)
        del(self.SD)
        del(self.SV)