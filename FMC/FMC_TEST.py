# TEST PROGRAM
# TO TEST COMMUNICATION, MOTION, AND SENSORS
# NO AP or etc

from communication import Communication
from motion import Motion
from global_var import *

C = Communication()
M = Motion()

C.init()
M.init()

C.run()

while True:
    try:
        M.change_to("elevator", command_list["LEVER_Y"])
        M.change_to("engine", (command_list["THRUST_1"], command_list["THRUST_2"]))
        M.change_to("rudder", command_list["RUDDER"])
        M.change_to("aileron", command_list["LEVER_X"])
    except:
        pass