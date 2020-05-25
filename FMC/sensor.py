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

class Sensor:
    def __init__(self):
        self.serve = True
        self.CAMERA = webCam()

    def run(self):
        pass

    def _service(self):
        while self.serve:
            global_var.video = self.CAMERA.arr_read()
        
    def __del__(self):
        self.serve = False
        sleep(0.2)
        