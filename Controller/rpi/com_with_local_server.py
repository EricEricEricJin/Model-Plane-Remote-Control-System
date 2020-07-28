"""
    Send levers value to local server
    Recv ALT, SLEED, BANK, PITCH from serverS
"""

import global_var
from socket import *
from threading import Thread
from struct import pack, unpack


RPI_DATA_ADDR = ("100.100.100.100", 2000)
LS_CMD_ADDR = ("110.110.110.110", 2000)


DATA_PACK_FORMAT = ""
CMD_PACK_FORMAT = ""

DATA_PACK_KEYS = [""]

class communicateWithLocalServer:
    def __init__(self):
        self.data_sock = socket(AF_INET, SOCK_STREAM)
        self.cmd_sock = socket(AF_INET, SOCK_STREAM)
        self.data_sock.bind(RPI_DATA_ADDR)
        self.serve = True

    def run(self):
        t_cmd = Thread(target = self._send_cmd)
        t_data = Thread(target = self._recv_data)
        t_cmd.start()
        t_data.start()

    def _send_cmd(self):
        while self.serve:
            try:
                self.cmd_sock.sendto(
                    pack(CMD_PACK_FORMAT, *list(global_var.datalist.values())),
                    LS_CMD_ADDR
                )
            except:
                pass

    def _recv_data(self):
        while self.serve:
            try:
                raw = self.data_sock.recv(1024)
                processed = unpack(DATA_PACK_FORMAT, raw)
                for i in range(len(DATA_PACK_KEYS)):
                    global_var.datalist[DATA_PACK_KEYS[i]] = processed[i]
            except:
                pass
