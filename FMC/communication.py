# read data and video from global_var and send them to server
# recv command from server and write them to global_var
from threading import Thread
from socket import *


SERVER_IP = "127.0.0.1"
VIDEO_PORT = 1140
DATA_PORT = 1910
CMD_PORT = 4470

CMD_MAX_RECV = 1024
CMD_PACK_FORMAT = "?Hh?H?Hhh?hh"
CMD_PACK_KEYS = [
    "AP_ALT_ON", "AP_ALT_VAL", "AP_VS_VAL",
    "AP_HDG_ON", "AP_HDG_VAL", 
    "AP_VOL_ON", "AP_VOL_VAL", 
    "LEVER_X", "LEVER_Y",
    "GEAR_DOWN",
    "THRUST_1", "THRUST_2",
    "MCAS_ON"
]

DATA_PACK_FORMAT = ""

class Socket:
    def __init__(self):
        self.serve = True
        self.my_socket = socket(AF_INET, SOCK_STREAM)
    
    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        self.my_socket.connect((ip, port))


    def send(self, data):
        pass

    def recv(self, MAX_RECV):
        pass

class Communication:
    