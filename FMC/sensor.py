from cv2 import cv2
from time import sleep
from threading import Thread
import global_var

crate = 5

class webCam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)


    def arr_read(self):

        ret, frame = self.cap.read()
        y, x = frame.shape[0:2]
        x = int(x / crate)
        y = int(y / crate)
        frame = cv2.resize(frame, (x, y))
        return frame

    def __del__(self):
        pass

class TOF:
    def __init__(self, iic_ins, addr):
        self.bus = iic_ins
        self.addr = addr

    def read(self):
        raw = self.bus.read_i2c_block_data(self.addr, 0x04)
        return (raw[0] - 128) * 256 + (raw[1] - 128)

    def __del__(self):
        pass


class Sensor:
    def __init__(self):
        self.serve = True
        self.CAMERA = webCam()

    def update(self):
        pass

    def __del__(self):
        self.serve = False
        sleep(0.2)

if __name__ == "__main__":
    S = Sensor()
