from threading import Thread
from motion import Motion
import global_var
# auto pilot
class autoPilot:
    def __init__(self):
        self.alt_on = False
        self.hdg_on = False
        self.vel_on = False

        self.alt_tar = None
        self.alt_vs = None

        self.hdg_tar = None
        self.vel_tar = None

    def init(self, motion_instance):
        self.MOTION = motion_instance
        pass

    def run(self):
        t = Thread(target = self._service, args = ())
        t.start()

    def _service(self):
        while True:
            if self.alt_on:
                self.MOTION.change_to("elevator", self._a2e(self.alt_tar - global_var.data_list["ALT"], self.alt_vs))
            if self.hdg_on:
                self.MOTION.change_to("rudder", self._h2r(self.hdg_tar - global_var.data_list["YAW"]))
            if self.vel_on:
                self.MOTION.change_to("engine", self._v2e(self.vel_tar - global_var.data_list["AIR_V"]))

    def __del__(self):
        pass

    def _a2e(self, delta_a, vs):
        if delta_a < 6:
            return (global_var.data_list["ENG_1"] + global_var.data_list["ENG_1"]) / 2
        else:
            return vs / 100 # vs has +/-

    def _h2r(self, delta_h):
        pass

    def _h2a(self, delta_h, row):
        pass

    def _v2e(self, delta_v):
        pass