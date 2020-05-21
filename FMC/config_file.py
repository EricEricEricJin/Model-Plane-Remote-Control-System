'''
    Created by Eric

    store configure values for the FMC program
'''

# ====== COMMUNICATION ======
SERVER_IP = "127.0.0.1"
VIDEO_PORT = 1140
DATA_PORT = 1910
CMD_PORT = 4470


CMD_MAX_RECV = 1024

CMD_PACK_FORMAT = "?Hh?H?Hhh?hh"
CMD_PACK_KEYS = [
    "AP_ALT_ON", "AP_ALT_VAL", "AP_VS_VAL",
    "AP_HDG_ON", "AP_HDG_VAL", 
    "AP_VOL_ON", "AP_VOL_VAL", 
    "LEVER_X", "LEVER_Y",
    "GEAR_DOWN",
    "THRUST_1", "THRUST_2",
    "MCAS_ON"
]

DATA_PACK_FORMAT = ""

VIDEO_QUALITY = 10
VIDEO_DEVICE = 0
VIDEO_CRATE = 100
VIDEO_DELAY = 0.1
# ============

# ====== MOTION ======
ESC_FREQ = 50
def ESC_PWR2DUTY(pwr):
    return (5 + 0.05 * pwr)

SERVO_FREQ = 50
def SERVO_DEG2DUTY(deg):
    return (deg - 2) * 18

ENGINE_1_BCM = 10
ENGINE_2_BCM = 11

RUDDER_BCM = 0
RUDDER_INIT = 90
RUDDER_MIN = 45
RUDDER_MAX = 135

ELEVATOR_1_BCM = 1
ELEVATOR_1_INIT = 90
ELEVATOR_1_MAX = 135
ELEVATOR_1_MIN = 45

ELEVATOR_2_BCM = 2
ELEVATOR_2_INIT = 90
ELEVATOR_2_MAX = 135
ELEVATOR_2_MIN = 45

AILERON_L_BCM = 3
AILERON_L_INIT = 90
AILERON_L_MIN = 45
AILERON_L_MAX = 135

AILERON_R_BCM = 4
AILERON_R_INIT = 90
AILERON_R_MIN = 45
AILERON_R_MAX = 135

GEAR_F_BCM = 5
GEAR_F_INIT = 90
GEAR_F_MIN = 45
GEAR_F_MAX = 135

GEAR_R_L_BCM = 6
GEAR_R_L_INIT = 0
GEAR_R_L_MIN = 0
GEAR_R_L_MAX = 90

GEAR_R_R_BCM = 7
GEAR_R_R_INIT = 0
GEAR_R_R_MIN = 0
GEAR_R_R_MAX = 90
# ============

'''
# ============ MCAS ============
def IS_STALL(vel, pitch, yaw, roll):
    # Examine whether is STALL
    return True

def IS_TO():
    # Examine whether is TO
    return True

def IS_LDG():
    # Examine whether is landing
    return True
'''

def rudder_pctg2deg(pctg):
    return 114514

def aileron_l_pctg2deg(pctg):
    return 1919810

def aileron_r_pctg2deg(pctg):
    return 114514

def elevator_l_pctg2deg(pctg):
    return 1919810

def elevator_r_pctg2deg(pctg):
    return 114514