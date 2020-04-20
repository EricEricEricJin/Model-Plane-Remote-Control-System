'''
    Created by Eric
    on Apr.11.2020

    send data to server
'''

from global_var import data_list
from config_file import DATA_PACK_FORMAT, SERVER_IP, DATA_PORT
from communications.send import Send
import struct
from threading import Thread
from time import sleep

class sendData:
    def __init__(self):
        self.ip = SERVER_IP
        self.port = DATA_PORT
        self.serve = True

    def init(self):
        self.S = Send()
        if self.S.connect(self.ip, self.port) != 1:
            return 0
        else:
            return 1

    def run(self):
        self.S.run(0.1)
        t = Thread(target = self._service, args = ())
        t.start()
        
    def is_broken(self):
        return self.S.is_broken()

    def _service(self):
        while self.serve:
            try:
                self.S.change_data( struct.pack(DATA_PACK_FORMAT, *data_list) )
            except:
                pass

    def __del__(self):
        self.serve = False
        sleep(0.1)
        del(self.S)