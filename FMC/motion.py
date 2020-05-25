# motion

import RPi.GPIO as GPIO
import global_var

ESC_FREQ = 50


SERVO_FREQ = 50

GEAR_F_BCM = 0
GEAR_F_UP = 0
GEAR_F_DOWN = 90

GEAR_R_L_BCM = 1
GEAR_R_L_UP = 0
GEAR_R_L_DOWN = 90

GEAR_R_R_BCM = 2
GEAR_R_R_UP = 0
GEAR_R_R_DOWN = 90

ENGINE_1_BCM = 3
ENGINE_2_BCM = 4

REV_1_BCM = 5
REV_1_OFF = 0
REV_1_ON = 90

REV_2_BCM = 6
REV_2_OFF = 0
REV_2_ON = 90

AILERON_L_BCM = 7
AILERON_L_INIT = 90
AILERON_R_BCM = 8
AILERON_R_INIT = 90
def aileron_l_val2deg(val):
    pass
def aileron_r_val2deg(val):
    pass

FLAPS_L_BCM = 9
FLAPS_L_INIT = 0
FLAPS_R_BCM = 10
FLAPS_R_INIT = 0
def flaps_l_val2deg(val):
    pass
def flaps_r_val2deg(val):
    pass


RUDDER_BCM = 11
RUDDER_INIT = 90
def rudder_val2deg(val):
    pass

ELEVATOR_L_BCM = 12
ELEVATOR_L_INIT = 90
ELEVATOR_R_BCM = 13
ELEVATOR_R_INIT = 90
def elevator_l_val2deg(val):
    pass

def elevator_r_val2deg(val):
    pass



class Esc:
    def __init__(self, BCM_PORT, init_pwr):
        GPIO.setup(BCM_PORT, GPIO.OUT)
        self.esc = GPIO.PWM(BCM_PORT, ESC_FREQ)
        self.esc.start(self._pwr2duty(init_pwr))
        
    def change_pwr(self, pwr):
        self.esc.ChangeDutyCycle(self._pwr2duty(pwr))

    def _pwr2duty(self, pwr):
        return (5 + 0.05 * pwr)

    def __del__(self):
        self.esc.stop()

class Servo:
    def __init__(self, BCM_PORT, init_deg):
        GPIO.setup(BCM_PORT, GPIO.OUT)
        self.servo = GPIO.PWM(BCM_PORT, SERVO_FREQ)
        self.servo.start(self._deg2duty(init_deg))

    def change_deg(self, deg):
        self.servo.ChangeDutyCycle(self._deg2duty(deg))

    def _deg2duty(self, deg):
        return (deg - 2) * 18

    def __del__(self):
        self.servo.stop()

class Motion:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.ENG_1 = Esc(ENGINE_1_BCM, 0)
        self.ENG_2 = Esc(ENGINE_2_BCM, 0)

        self.REV_1 = Servo(REV_1_BCM, REV_1_OFF)
        self.REV_2 = Servo(REV_2_BCM, REV_2_OFF)

        self.AILERON_L = Servo(AILERON_L_BCM, AILERON_L_INIT)
        self.AILERON_R = Servo(AILERON_R_BCM, AILERON_R_INIT)

        self.FLAPS_L = Servo(FLAPS_L_BCM, FLAPS_L_INIT)
        self.FLAPS_R = Servo(FLAPS_R_BCM, FLAPS_R_INIT)

        self.RUDDER = Servo(RUDDER_BCM, RUDDER_INIT)
        
        self.ELEVATOR_L = Servo(ELEVATOR_L_BCM, ELEVATOR_L_INIT)
        self.ELEVATOR_R = Servo(ELEVATOR_R_BCM, ELEVATOR_R_INIT)

        self.GEAR_F = Servo(GEAR_F_BCM, GEAR_F_DOWN)
        self.GEAR_R_L = Servo(GEAR_R_L_BCM, GEAR_R_L_DOWN)
        self.GEAR_R_R = Servo(GEAR_R_R_BCM, GEAR_R_R_DOWN)

    def change_pwr(self, pwr_1, pwr_2): # 0 ~ 100
        self.ENG_1.change_pwr(pwr_1)
        self.ENG_2.change_pwr(pwr_2)
        global_var.data_list["ENG_1"] = int(pwr_1)
        global_var.data_list["ENG_2"] = int(pwr_2)

    def change_aileron(self, val): # -1 ~ 1
        self.AILERON_L.change_deg(aileron_l_val2deg(val))
        self.AILERON_R.change_deg(aileron_r_val2deg(val))
        global_var.data_list["AILERON"] = int(100 * val)

    def change_rudder(self, val): # -1 ~ 1
        self.RUDDER.change_deg(rudder_val2deg(val))
        global_var.data_list["RUDDER"] = int(100 * val)

    def change_elevator(self, val): # -1 ~ 1
        self.ELEVATOR_L.change_deg(elevator_l_val2deg(val))
        self.ELEVATOR_R.change_deg(elevator_r_val2deg(val))
        global_var.data_list["ELEVATOR"] = int(100 * val)

    def change_flaps(self, val): # 0 - 30
        self.FLAPS_L.change_deg(flaps_l_val2deg(val))
        self.FLAPS_R.change_deg(flaps_r_val2deg(val))
        global_var.data_list["FLAPS"] = int(val)

    def turn_rev_1_on(self):
        self.REV_1.change_deg(REV_1_ON)
        global_var.data_list["REV_1"] = True

    def turn_rev_1_off(self):
        self.REV_1.change_deg(REV_1_OFF)
        global_var.data_list["REV_1"] = False

    def turn_rev_2_on(self):
        self.REV_2.change_deg(REV_2_ON)
        global_var.data_list["REV_2"] = True

    def turn_rev_2_off(self):
        self.REV_2.change_deg(REV_2_OFF)
        global_var.data_list["REV_2"] = False

    def gear_down(self):
        self.GEAR_F.change_deg(GEAR_F_DOWN)
        self.GEAR_R_L.change_deg(GEAR_R_L_DOWN)
        self.GEAR_R_R.change_deg(GEAR_R_R_DOWN)
        global_var.data_list["GEAR_DOWN"] = True

    def gear_up(self):
        self.GEAR_F.change_deg(GEAR_F_UP)
        self.GEAR_R_L.change_deg(GEAR_R_L_UP)
        self.GEAR_R_R.change_deg(GEAR_R_R_UP)
        global_var.data_list["GEAR_DOWN"] = False