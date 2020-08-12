# main logic and AP and so on
from communication import Communication
from motion import Motion
from sensor import Sensor
from ap import AP
from manual import Manual
from fdr import flightDataRecorder



import global_var

class Main():
    def __init__(self):
        self.Communication_ins = Communication()
        self.Motion_ins = Motion()
        self.Sensor_ins = Sensor()        
        self.AP_ins = AP(self.Motion_ins)
        self.Manual_ins = Manual(self.Motion_ins)
        self.FDR_ins = flightDataRecorder()

    def run(self):
        while True:
            # Update Sensor
            self.Sensor_ins.update()

            # Update Motion
            if global_var.command_list["AP_VEL_ON"] == True:
                self.AP_ins.update_engine()
            else:
                self.Manual_ins.update_engine()

            if global_var.command_list['AP_ALT_ON'] == True:
                self.AP_ins.update_elevator()
            else:
                self.Manual_ins.update_elevator()

            if global_var.command_list["AP_HDG_ON"] == True:
                self.AP_ins.update_aileron()
            else:
                self.Manual_ins.update_aileron()

            self.Manual_ins.update_rudder()
            
            # Update FDR
            self.FDR_ins.update()





if __name__ == "__main__":
    MAIN = Main()
    MAIN.run()
