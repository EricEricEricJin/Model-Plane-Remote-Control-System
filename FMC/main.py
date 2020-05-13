from communication import Communication
from sensor import Sensor
from motion import Motion
from ap import autoPilot
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
        self.AP = autoPilot()

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

        self.AP.init(self.MOTION)

    def run(self):
        self.COMMUNICATION.run()
        self.SENSOR.run()
        self.AP.run()

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
                    self.AP.alt_tar = command_list["AP_ALT_VAL"]
                    self.AP.alt_vs = command_list["AP_VS_VAL"]
                    self.AP.alt_on = True
                    
                else:
                    # turn off alt ap
                    self.AP.alt_on = False
                    self.MOTION.change_to("ELEVATOR", lever_y2elevator(command_list["LEVER_Y"]))

                if command_list["AP_HDG_ON"]:
                    self.AP.hdg_tar = command_list["AP_HDG_VAL"]
                    self.AP.hdg_on = True
                    
                else:
                    self.AP.hdg_on = False
                    self.MOTION.change_to("RUDDER", lever_x2rudder(command_list["LEVER_X"]))
                    # self.MOTION.change_to("AILERON", 114)
                
                if command_list["AP_VEL_ON"]:
                    self.AP.vel_tar = command_list["AP_VEL_VAL"]
                    self.AP.vel_on = True
                    
                else:
                    self.AP.vel_on = False
                    self.MOTION.change_to("ENGINE", (command_list["THRUST_1"], command_list["THRUST_2"]))