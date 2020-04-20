'''
    Test of video transmition
'''

from communication import Communication
from sensor import Sensor
import global_var
from cv2 import cv2
from time import sleep
if __name__ == "__main__":
    C = Communication()
    S = Sensor()
    C.init()
    S.init()
    C.run()
    S.run()
    
    '''
    while True:
        # global video
        # print(global_var.video)
        try:
            cv2.imshow("local", global_var.video)
        except Exception as e:
            print("imshow exc", e)
            pass
        k = cv2.waitKey(5)& 0xFF
        if k==27:
            break
        sleep(0.04)
    # del(C)
    del(S)
    '''