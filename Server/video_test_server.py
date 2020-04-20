from time import sleep

from switch import Switch

video_switch = Switch("127.0.0.1", 1234, 2345, 20480)
# data_switch = Switch("127.0.0.1", 2345, 2346, 1024)
# cmd_switch = Switch("127.0.0.1", 3456, 3457, 1024)
video_switch.run()
# data_switch.run()
# cmd_switch.run()
