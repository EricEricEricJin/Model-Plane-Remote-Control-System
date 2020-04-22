from communication import Communication
from sensor import Sensor
from motion import Motion

class Main:
    def __init__(self):
        pass

    def init(self):
        self.COMMUNICATION = Communication()
        self.SENSOR = Sensor()
        self.MOTION = Motion()

        if self.COMMUNICATION.init() == 1:
            print("communication module start success")
        else:
            print("communication module start failure")

        if self.MOTION.init() == 1:
            print("motion module start success")
        else:
            print("motion module start failure")

        if self.SENSOR.init() == 1:
            print("sensor module start success")
        else:
            print("sensor module start failure")

    def run(self):
        self.COMMUNICATION.run()
        self.SENSOR.run()

        
    