from motion import Motion
from global_var import *
from threading import Thread

class inDirect:
    def __init__(self, motion_ins):
        self.serve = True
        
        self.motion_ins = motion_ins
        self.engine_act = False
        self.elevator_act = False
        self.aileron_act = False
        self.rudder_act = False

        self.elevator_turnon = False
        self.aileron_turnon = False

        self.speed_tar = 0
        self.pitch_tar = 0
        self.roll_tar = 0
        
        t = Thread(target = self._service)
        t.start()


    def change_status(self, engine, elevator, aileron_and_rudder):
        self.engine_act = engine
        if elevator and (not self.elevator_act):
            self.elevator_turnon = True
        self.elevator_act = elevator
        if aileron_and_rudder and (not self.aileron_act):
            self.aileron_turnon = True
        self.aileron_act = aileron_and_rudder
        self.rudder_act = aileron_and_rudder

    def _service(self):
        while self.serve:
            if self.engine_act:
                self.speed_tar = command_list["THR_ 1"]
                # adjust to speed tar
                
            if self.elevator_act:
                if self.elevator_turnon:
                    self.pitch_tar = data_list["PITCH"]
                    self.elevator_turnon = False
                self.pitch_tar += command_list["LEVER_Y"] / 100
                # adjust to pitch
                self.motion_ins.change_elevator(self._pitch_diff_2_ele(self.pitch_tar - data_list["PITCH"]))

            if self.aileron_act:
                if self.aileron_turnon:
                    self.roll_tar = data_list["ROLL"]
                    self.aileron_turnon = False
                self.roll_tar += command_list["LEVER_X"] / 100
                # adjuct to roll
                self.motion_ins.change_aileron(self._roll_diff_2_ail(self.roll_tar - data_list["ROLL"]))
            
            if self.rudder_act:
                # set to 0
                self.motion_ins.change_rudder(0)
                
    def _roll_diff_2_ail(self, diff): # diff: tar - actual
        val = 0.1 * diff
        if val > 1:
            val = 1
        elif val < -1:
            val = -1
        return val

    def _pitch_diff_2_ele(self, diff):
        val = 0.1 * diff
        if val > 1:
            val = 1
        elif val < -1:
            val = -1
        return val