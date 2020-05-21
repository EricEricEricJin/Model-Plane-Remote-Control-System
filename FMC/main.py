from communication import Communication
from sensor import Sensor
from motion import Motion
from ap import autoPilot
from global_var import *
from config_file import *


def lever_y2elevator(y):
    # 侧杆y轴幅度转升降舵角度
    return y

def rudder2ail(r):
    return r


def lever_x2ail(x):
    return x

def stall():
    return True

def deep_stall():
    return True

def roll2ail(r):
    return 11.4514

def rudder2rudder(r):
    return 11.4


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
            if (stall() and command_list["MCAS_ON"] and (not command_list["GEAR_DOWN"])):
                if deep_stall():
                    self.AP.alt_on = False
                    self.AP.hdg_on = False
                    self.AP.vel_on = False

                else:
                    self.MOTION.change_to("elevator", -100)
                    self.MOTION.change_to("engine", (100, 100))
                    self.MOTION.change_to("aileron", roll2ail(data_list["ROLL"]))
            else:
                if command_list["AP_ALT_ON"]:
                    self.AP.alt_tar = command_list["AP_ALT_VAL"]
                    self.AP.alt_vs = command_list["AP_VS_VAL"]
                    self.AP.alt_on = True
                    
                else:
                    # turn off alt ap
                    self.AP.alt_on = False
                    self.MOTION.change_to("elevator", lever_y2elevator(command_list["LEVER_Y"]))                
                
                if command_list["AP_HDG_ON"]:
                    self.AP.hdg_tar = command_list["AP_HDG_VAL"]
                    self.AP.hdg_on = True
                    
                else:
                    self.AP.hdg_on = False
                    self.MOTION.change_to("rudder", rudder2rudder(command_list["RUDDER"]))
                    self.MOTION.change_to("aileron", rudder2ail(rudder2rudder(command_list["RUDDER"])))

                if command_list["AP_VEL_ON"] == True:
                    self.AP.vel_tar = command_list["AP_VEL_VAL"]
                    self.AP.vel_on = True
                else:
                    self.AP.vel_on = False
                    self.MOTION.change_to("engine", (command_list["THRUST_1"], command_list["THRUST_2"]))
