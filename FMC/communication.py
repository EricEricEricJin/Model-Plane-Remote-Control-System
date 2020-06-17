# read data and video from global_var and send them to server
# recv command from server and write them to global_var

# use UDP

from threading import Thread
from socket import *
import numpy as np
import struct
import global_var
from cv2 import cv2
from time import sleep, time



SERVER_IP = "127.0.0.1"
VIDEO_PORT = 2000
DATA_PORT = 2100
CMD_PORT = 2200
CMD_HBP = 2300

CMD_MAX_RECV = 1024
CMD_PACK_FORMAT = "?Hh?H?Hhhh?HH??"
CMD_PACK_KEYS = [
    "AP_ALT_ON", "AP_ALT_VAL", "AP_VS_VAL",
    "AP_HDG_ON", "AP_HDG_VAL",
    "AP_VEL_ON", "AP_VEL_VAL",
    "LEVER_X", "LEVER_Y",
    "RUDDER",
    "GEAR_DOWN",
    "THRUST_1", "THRUST_2",
    "MCAS_ON",
    "INDIRECT"
]

DATA_PACK_FORMAT = "hHhhHhHHH??hhhH?"


class udpSocket:
    def __init__(self, server_ip, data_port, max_recv, heartBit_port = None):
        self.my_sock = socket(AF_INET, SOCK_DGRAM)

        self.data_addr = (server_ip, data_port)
        self.heartBit_addr = (server_ip, heartBit_port)

        self.max_recv = max_recv

    def send(self, data):
        self.my_sock.sendto(data, self.data_addr)

    def recv(self):
        # print("udpsock recv")
        return self.my_sock.recv(self.max_recv)

    def send_heartBit(self):
        self.my_sock.sendto(b"", self.heartBit_addr)

    def __del__(self):
        self.serve = False
        self.my_sock.close()



class Communication:
    def __init__(self):
        self.video_sock = udpSocket(SERVER_IP, VIDEO_PORT, 40960)
        self.data_sock = udpSocket(SERVER_IP, DATA_PORT, 1024)
        self.cmd_sock = udpSocket(SERVER_IP, CMD_PORT, 1024, heartBit_port = CMD_HBP)
        self.serve = True

        self.last_bit_time = None


    def run(self):
        t_recving = Thread(target = self._recving)
        t_sending = Thread(target = self._sending)

        self.cmd_sock.send_heartBit()
        self.last_bit_time = time()
        t_recving.start()
        t_sending.start()


    def _recving(self):
        while self.serve:
            if time() - self.last_bit_time > 1:
                self.cmd_sock.send_heartBit()
                self.last_bit_time = time()

            recv_raw = self.cmd_sock.recv()
            # print("RAW:", recv_raw)
            try:
                recv_unpacked = struct.unpack(CMD_PACK_FORMAT, recv_raw)
                # print("UNPACKED", recv_unpacked)
                for i in range(len(CMD_PACK_KEYS)):
                    global_var.command_list[CMD_PACK_KEYS[i]] = recv_unpacked[i]
            except Exception as e:
                print(e)

            # print("CMD", global_var.command_list)


    def _sending(self):
        while self.serve:
            try:
                print(global_var.command_list)
                packed_data = struct.pack(DATA_PACK_FORMAT, *list(global_var.data_list.values()))
                self.data_sock.send(packed_data)
                img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10] # Video quality = 10
                _, bi = cv2.imencode(".jpg", global_var.video, params = img_param)
                bi = np.array(bi)
                bi = bi.tostring()
                self.video_sock.send(bi)
                # print("Video and data sent")
            except Exception as e:
                print("Video send exception:", e)
                pass
            sleep(0.05)

    def __del__(self):
        self.serve = False
        del(self.video_sock)
        del(self.data_sock)
        del(self.cmd_sock)


if __name__ == "__main__":
    ComTest = Communication()
    ComTest.run()
