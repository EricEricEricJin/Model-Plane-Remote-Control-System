import global_var
import pitch_limit

class AP:
    def __init__(self, motion_ins):
        self.motion_ins = motion_ins

    def update_engine(self):
        if abs(global_var.command_list["AP_VEL_VAL"] - global_var.data_list["AIR_V"] > 3):
            tar_accel = (global_var.command_list["AP_VEL_VAL"] - global_var.data_list["AIR_V"]) / 5
            pwr = (global_var.data_list["ENG_0"] + global_var.data_list["ENG_1"]) / 2 + (tar_accel - global_var.data_list["ACCEL"])
            self.motion_ins.change_pwr(pwr, pwr)

    def update_elevator(self):
        if abs(global_var.command_list["AP_ALT_VAL"] - global_var.data_list["ALT"]) > 5:
            tar_ele = (global_var.command_list["AP_ALT_VS"] - global_var.data_list["VS"]) / 100
        else:
            tar_ele = - global_var.data_list["VS"] / 100

        
        if global_var.data_list["PITCH"] > pitch_limit.max_pitch():
            tar_ele = -0.1

        if tar_ele > 1:
                tar_ele = 1
        elif tar_ele < -1:
            tar_ele = -1
        
        self.motion_ins.change_elevator(tar_ele)

    def update_aileron(self):
        # hdg to roll
        if abs(global_var.command_list["AP_HDG_VAL"] - global_var.data_list["HDG"]) > 3:
            tar_ail = (global_var.command_list["AP_HDG_TURNRATE"] - global_var.data_list["TURN_RATE"]) / 10
        else:
            tar_ail = - global_var.data_list["TURN_RATE"] / 100

        if tar_ail > 1:
            tar_ail = 1
        elif tar_ail < -1:
            tar_ail = -1

        self.motion_ins.change_aileron(tar_ail)

        