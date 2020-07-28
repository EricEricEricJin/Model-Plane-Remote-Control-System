from global_var import command_list
from threading import Thread

class Direct:
    def __init__(self, motion_ins):
        self.motion_ins = motion_ins
        self.engine_act = False
        self.elevator_act = False
        self.aileron_act = False
        self.rudder_act = False
        
        self.serve = True
        t = Thread(target = self._service)
        t.start()


    def _service(self):
        while self.serve:
            if self.engine_act:
                self.motion_ins.change_pwr(command_list["THRUST_1"], command_list["THRUST_2"])
            if self.elevator_act:
                self.motion_ins.change_elevator(command_list["LEVER_Y"] / 255)
            if self.aileron_act:
                self.motion_ins.change_aileron(command_list["LEVER_X"] / 255)
            if self.rudder_act:
                self.motion_ins.change_rudder(command_list["RUDDER"] / 255)


    def change_status(self, engine, elevator, aileron, rudder):
        self.engine_act = engine
        self.elevator_act = elevator
        self.aileron_act = aileron
        self.rudder_act = rudder