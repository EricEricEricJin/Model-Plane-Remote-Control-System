'''
    Created by Eric
    on Apr.11.2020

    receive command from server
'''

from global_var import command_list
from config_file import CMD_PACK_FORMAT, CMD_PACK_KEYS, SERVER_IP, CMD_PORT, CMD_MAX_RECV
from communications.receive import Receive
import struct
from threading import Thread
from time import sleep

class receiveCmd:
    def __init__(self):
        self.ip = SERVER_IP
        self.port = CMD_PORT
        self.serve = True
        pass

    def init(self):
        self.R = Receive()
        if self.R.connect(self.ip, self.port) != 1:
            return 0
        else:
            self.isBroken = False
            return 1

    def run(self):
        self.R.run(CMD_MAX_RECV)
        t = Thread(target = self._service, args = ())
        t.start()

    def is_broken(self):
        return self.R.is_broken()

    def _service(self):
        while self.serve:
            try:
                raw = self.R.get_data()
                psd = struct.unpack(CMD_PACK_FORMAT, raw)
                for i in range(len(CMD_PACK_KEYS)):
                    command_list[CMD_PACK_KEYS[i]] = psd[i]
            except:
                pass

    def __del__(self):
        self.serve = False
        sleep(0.1)
        del(self.R)