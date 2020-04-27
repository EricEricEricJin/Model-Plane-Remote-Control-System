from communication import Communication
from sensor import Sensor
from motion import Motion
from global_var import *
from config_file import *


def lever_y2elevator(y):
    # 侧杆y轴幅度转升降舵角度
    return y

def rudder2ali(r):
    return r


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

            # How to say its taking off / landing?
            # set a timeout: after n secs can;t roll out -> ap / manue
            if (not (IS_LDG() and data_list["ALT"] < 3)) and IS_STALL(data_list["AIR_V"], data_list["PITCH"], data_list["YAW"], data_list["ROLL"]):
                # HOW TO DO WHEN STALL
                self.MOTION.change_to("ENGINE", (1, 1)) # TOGA THRUST
                self.MOTION.change_to("ELEVATOR", -1)
                self.MOTION.change_to("RUDDER", 0)
                
            else:
                
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
                    self.MOTION.change_to("AILERON", 114)
                if command_list["AP_VEL_ON"]:
                    # turn on velocity
                    pass
                else:
                    self.MOTION.change_to("ENGINE", (command_list["THRUST_1"], command_list["THRUST_2"]))