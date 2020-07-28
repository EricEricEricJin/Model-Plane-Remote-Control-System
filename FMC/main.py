# main logic and AP and so on
from communication import Communication
from motion import Motion
from sensor import Sensor
from indirect import inDirect
from ap import AP
from mcas import MCAS
from direct import Direct


import global_var

class Main():
    def __init__(self):
        self.Communication_ins = Communication()
        self.Motion_ins = Motion()
        self.Sensor_ins = Sensor()
        self.inDirect_ins = inDirect(self.Motion_ins)
        self.AP_ins = AP(self.Motion_ins)
        self.MCAS_ins = MCAS(self.Motion_ins)
        self.Direct_ins = Direct(self.Motion_ins)


    def run(self):
        indirect_status = [None, None, None]
        ap_status = [None, None, None]
        mcas_on = None
        direct_status = [None, None, None, None]

        while True:
            if global_var.command_list["MCAS_ON"] == True:
                mcas_on = True
            else:
                mcas_on = False

            if global_var.command_list["AP_ALT_ON"] == True:
                indirect_status[1] = False
                ap_status[1] = True
                direct_status[1] = False

            elif global_var.command_list["INDIRECT"] == True:
                indirect_status[1] = True
                ap_status[1] = False
                direct_status[1] = False

            else:
                indirect_status[1] = False
                ap_status[1] =  False
                direct_status[1] = True

            if global_var.command_list["AP_HDG_ON"] == True:
                indirect_status[2] = False
                ap_status[2] =  True
                direct_status[2] = False
                direct_status[3] = False
            elif global_var.command_list["INDIRECT"] == True:
                indirect_status[2] = True
                ap_status[2] =  False
                direct_status[2] = False
                direct_status[3] = False
            else:
                indirect_status[2] = False
                ap_status[2] =  False
                direct_status[2] = True
                direct_status[3] = True

            if global_var.command_list["AP_VEL_ON"] == True:
                indirect_status[0] = False
                ap_status[0] =  True
                direct_status[0] = False
            elif global_var.command_list["INDIRECT"] == True:
                indirect_status[0] = True
                ap_status[0] =  False
                direct_status[0] = False

            else:
                indirect_status[0] = False
                ap_status[0] =  False
                direct_status[0] = True

            if self.MCAS_ins.is_engaging() == True:
                indirect_status = [False, False, False]
                ap_status = [False, False, False]
                direct_status = [False, False, False, False]

            self.inDirect_ins.change_status(*indirect_status)
            self.AP_ins.change_status(*ap_status)
            self.Direct_ins.change_status(*direct_status)

if __name__ == "__main__":
    MAIN = Main()
    MAIN.run()
