from motions.engine import Engine
from motions.servo import Servo
from config_file import *

class Motion:
    def __init__(self):
        self.ENGINE = Engine()
        self.RUDDER = Servo()
        self.AILERON_L = Servo()
        self.AILERON_R = Servo()
        self.ELEVATOR_L = Servo()
        self.ELEVATOR_R = Servo()

    def init(self):
        try:
            self.ENGINE.init()
            self.RUDDER.init(RUDDER_BCM, SERVO_FREQ, RUDDER_INIT)
            self.AILERON_L.init(AILERON_L_BCM, SERVO_FREQ, AILERON_L_INIT)
            self.AILERON_R.init(AILERON_R_BCM, SERVO_FREQ, AILERON_R_INIT)
            self.ELEVATOR_L.init(ELEVATOR_L_BCM, SERVO_FREQ, ELEVATOR_L_INIT)
            self.ELEVATOR_R = init(ELEVATOR_R_BCM, SERVO_FREQ, ELEVATOR_R_INIT)
            return 1
        except:
            return 0

    def change_to(self, key, val):
        # key: "elevator", xxx
        # val: value
        if key == "rudder":
            self.RUDDER.change_deg(rudder_pctg2deg(val))
        elif key == "aileron":
            self.AILERON_L.change_deg(aileron_l_pctg2deg(val))
            self.AILERON_R.change_deg(aileron_r_pctg2deg(val))
        elif key == "elevator":
            self.ELEVATOR_L.change_deg(elevator_l_pctg2deg(val))
            self.ELEVATOR_R.change_deg(elevator_r_pctg2deg(val))
        elif key == "engine":
            self.ENGINE.change_pwr((val[0], val[1]))

    def __del__(self):
        pass