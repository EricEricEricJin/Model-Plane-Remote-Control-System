from cv2 import cv2
from time import sleep

from video_decode import video_decode
from communication.receive import Receive

RecvController = Receive()

ip = "127.0.0.1"
# ip = "45.249.94.168"
if RecvController.connect(ip, 5140) == 0:
    print("CAN'T CONNECT!")



RecvController.run(20480)

while True:
    frame_get = RecvController.get_data()
    print(frame_get)
    if frame_get != None:
        try:
            frame_get = video_decode(frame_get)
            cv2.imshow("recv", frame_get)
        except:
            pass
    k = cv2.waitKey(5)& 0xFF
    if k==27:
        break
    sleep(0.04)

del(RecvController)
