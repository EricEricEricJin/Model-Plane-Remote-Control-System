import global_var
from threading import Thread
from pitch_limit import max_pitch

class Manual:
    def __init__(self, motion_ins):
        self.motion_ins = motion_ins        

    def update_engine(self):
        self.motion_ins.change_pwr(global_var.command_list["THRUST_1"], global_var.command_list["THRUST_2"])

    def update_elevator(self):
        if global_var.data_list["PITCH"] > max_pitch() and global_var.command_list["MCAS_ON"]:
            self.motion_ins.change_elevator(-0.1)
        else:
            self.motion_ins.change_elevator(global_var.command_list["LEVER_Y"] / 255)

    def update_aileron(self):
        self.motion_ins.change_aileron(global_var.command_list["LEVER_X"] / 255)

    def update_rudder(self):
        self.motion_ins.change_rudder(global_var.command_list["RUDDER"] / 255)