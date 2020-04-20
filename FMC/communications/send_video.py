'''
    Created by Eric
    on Apr.11.2020

    send video to server
'''

import sys
import os
sys.path.append("..")

# from global_var import video
import global_var
from config_file import SERVER_IP, VIDEO_PORT, VIDEO_QUALITY
from communications.send import Send
import numpy as np
from cv2 import cv2
from time import sleep
from threading import Thread
class sendVideo:
    def __init__(self):
        self.ip = SERVER_IP
        self.port = VIDEO_PORT

        self.serve = True
        # print("send video_ video", video)

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
                img_param = [int(cv2.IMWRITE_JPEG_QUALITY), VIDEO_QUALITY]
                _, bi = cv2.imencode(".jpg", global_var.video, params = img_param)
                bi = np.array(bi)
                bi = bi.tostring()
                self.S.change_data(bi)
            except:
                pass

    def __del__(self):
        self.serve = False
        sleep(0.1)
        del(self.S)