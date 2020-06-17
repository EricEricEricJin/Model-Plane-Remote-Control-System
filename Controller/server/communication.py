# use UDP

from threading import Thread
from socket import *
import struct
from numpy import fromstring
from numpy import uint8
import global_var
from cv2 import cv2
from time import sleep, time



SERVER_IP = "127.0.0.1"

VIDEO_PORT = 2400
VIDEO_HBP = 2500

DATA_PORT = 2600
DATA_HBP = 2700

CMD_PORT = 2800


CMD_PACK_FORMAT = "?Hh?H?Hhhh?HH??"


DATA_PACK_FORMAT = "hHhhHhHHH??hhhH?"
DATA_PACK_KEYS = [
    "PITCH", "YAW", "ROLL",
    "ALT", "RADIO_H",
    "AIR_V", "GROUND_V",

    "ENG_1", "ENG_2",
    "REV_1", "REV_2",
    "RUDDER",
    "ELEVATOR",
    "AILERON",
    "FLAPS",
    "GEAR_DOWN"
]

class udpSocket:
    def __init__(self, server_ip, data_port, max_recv, heartBit_port = None):
        self.my_sock = socket(AF_INET, SOCK_DGRAM)

        self.data_addr = (server_ip, data_port)
        self.heartBit_addr = (server_ip, heartBit_port)

        self.max_recv = max_recv

    def send(self, data):
        self.my_sock.sendto(data, self.data_addr)

    def recv(self):
        return self.my_sock.recv(self.max_recv)

    def send_heartBit(self, heartBit_content = b""):
        self.my_sock.sendto(heartBit_content, self.heartBit_addr)

    def __del__(self):
        self.serve = False
        self.my_sock.close()


class Communication:
    def __init__(self):
        self.serve = True
        self.last_bit_time = 0
        self.video_sock = udpSocket(SERVER_IP, VIDEO_PORT, 40960, heartBit_port = VIDEO_HBP)
        self.data_sock = udpSocket(SERVER_IP, DATA_PORT, 1024, heartBit_port = DATA_HBP)
        self.cmd_sock = udpSocket(SERVER_IP, CMD_PORT, 1024)

    def run(self):
        t_recv_v = Thread(target = self._recv_v)
        t_recv_d = Thread(target = self._recv_d)
        t_send = Thread(target = self._send)
        t_recv_v.start()
        t_recv_d.start()
        t_send.start()

    def _recv_v(self):
        while self.serve:
            if time() - self.last_bit_time > 1:
                self.video_sock.send_heartBit(b"v")
            recv_raw = self.video_sock.recv()
            # print("Raw:", recv_raw)
            try:
                decoded = cv2.imdecode(fromstring(recv_raw, uint8), cv2.IMREAD_COLOR)
                global_var.video = decoded
                # print(decoded)
            except Exception as e:
                print("Video decode exception:", e)

    def _recv_d(self):
        while self.serve:
            if time() - self.last_bit_time > 1:
                self.data_sock.send_heartBit(b"d")
                self.last_bit_time = time()
            recv_raw = self.data_sock.recv()
            recv_unpacked = struct.unpack(DATA_PACK_FORMAT, recv_raw)
            for i in range(len(DATA_PACK_KEYS)):
                global_var.data_list[DATA_PACK_KEYS[i]] = recv_unpacked[i]

    def _send(self):
        while self.serve:
            self.cmd_sock.send(struct.pack(CMD_PACK_FORMAT, *list(global_var.command_list.values())))


if __name__ == "__main__":
    ComTest = Communication()
    ComTest.run()

    while True:
        print(global_var.data_list)
        try:
            cv2.imshow("recv", global_var.video)
            print('IM SHOW')
        except:
            pass
        k = cv2.waitKey(5)& 0xFF
        if k==27:
            break
        sleep(0.04)
