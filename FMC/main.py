from communication import Communication
from sensor import Sensor
from motion import Motion
from global_var import *


def lever_y2elevator(y):
    # 侧杆y轴幅度转升降舵角度
    return y

def lever_x2rudder(x):
    return x

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
        while True:
            if command_list["AP_ALT_ON"]:
                # turn on alt ap
                pass
            else:
                # turn off alt ap
                self.MOTION.change_to("ELEVATOR", lever_y2elevator(command_list["LEVER_Y"]))

            if command_list["AP_HDG_ON"]:
                # turn on hdg ap
                pass
            else:
                # turn off hdg ap
                self.MOTION.change_to("RUDDER", lever_x2rudder(command_list["LEVER_X"]))

            