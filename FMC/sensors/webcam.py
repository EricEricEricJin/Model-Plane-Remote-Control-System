'''
    Created by Eric
    on Mar.28

    web camera module
'''

import sys
import os
sys.path.append("..")
# sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
# print("path", sys.path)
from cv2 import cv2
from time import sleep
from config_file import VIDEO_CRATE, VIDEO_DEVICE, VIDEO_PORT, VIDEO_QUALITY, VIDEO_DELAY
from threading import Thread
import global_var


class webCam:
    def __init__(self):
        self.device = VIDEO_DEVICE
        self.crate = VIDEO_CRATE
        self.delay = VIDEO_DELAY

        self.serve = True
        self.isBroken = True
        

    def init(self):
        try:
            self.cap = cv2.VideoCapture(self.device)
            self.isBroken = False
            print("CAM INIT SUCCESS")
            return 1
        except:
            return 0

    def run(self):
        t = Thread(target = self._service, args = ())
        t.start()

    def _service(self):
        # global video
        while self.serve:
            try:
                # print("video in webcam", video)
                # FMC.global_var.video = self._arr_read()
                global_var.video = self._arr_read()
                sleep(self.delay)
                if self.isBroken == True:
                    self.isBroken = False
            except:
                print("webcam exception")
                self.isBroken = True
        

    def is_broken(self):
        return self.isBroken

    def _arr_read(self):
        ret, frame = self.cap.read()
        # print(frame.size)
        y, x = frame.shape[0:2]
        x = int(x / self.crate)
        y = int(y / self.crate)
        frame = cv2.resize(frame, (x, y))
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame

    def __del__(self):
        self.serve = False
        sleep(self.delay)

