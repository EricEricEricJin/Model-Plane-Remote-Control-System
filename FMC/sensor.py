'''
    Created by Eric
    on Apr.11.2020

    Sensor program
'''

from sensors.webcam import webCam

class Sensor:
    def __init__(self):
        self.WC = webCam()

    def init(self):
        self.WC.init()

    def run(self):
        self.WC.run()

    def __del__(self):
        del(self.WC)