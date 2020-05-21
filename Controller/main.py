from UI.ui import UI
from communication.receive import Receive
from communication.send import Send

from video_decode import video_decode

from threading import Thread
from time import sleep

import config_file

class Main:
    def __init__(self):
        pass
    def start_ui_and_check(self):
        self.ui = UI()
        self.ui.run()
        self.ui.ui_checklist()

        t_ui = Thread(target = self._ui_service, args = ())
        t_ui.start()
    
    def _ui_service(self):
        pass
    
    def connect_to_server_and_start_service(self):
        self.send_cmd = Send()
        self.recv_data = Receive()
        self.recv_video = Receive()

        if self.send_cmd.connect(self.c_ip, self.c_port) != 1:
            pass
        else:
            self.send_cmd.run(0.1)
            self.msg_send_to_ui["connection"]["cmd"] = True
        
        if self.recv_data.connect(self.d_ip, self.d_port) != 1:
            pass
        else:
            self.recv_data.run(1024)
            self.msg_send_to_ui["connection"]["data"] = True

        if self.recv_video.connect(self.v_ip, self.v_port) != 1:
            pass
        else:
            self.recv_video.run(4096)
            self.msg_send_to_ui["connection"]["video"] = True

        
    def start_main_function(self):
        t_send = Thread(target = self._send_service, args = ())
        t_recv = Thread(target = self._recv_service, args = ())
        t_conn_guard = Thread(target = self._conn_guard_service, args = ())
        
        t_send.start()
        t_recv.start()
        t_conn_guard.start()

    def _recv_service(self):
        # get data and decode and send to UI
        while self.all_serve:
            if self.communication_serve:
                try:
                    data = self.recv_data.get_data().decode("utf-8")
                    video = self.recv_video.get_data()
                    video = video_decode(video)

                    self.msg_send_to_ui["video"] = video
                    self.msg_send_to_ui["data"] = data
                except:
                    pass
        
    def _send_service(self):
        # get cmd from UI and encode and send to server
        while self.all_serve:
            if self.communication_serve:
                self.send_cmd.change_data(str(self.msg_recv_from_ui["operation"]).encode("utf-8"))

    def _conn_guard_service(self):
        while self.all_serve:
            if self.communication_serve:
                if self.recv_data.is_broken() == True:
                    self.msg_send_to_ui["connection"]["data"] = False
                else:
                    self.msg_send_to_ui["connection"]["data"] = True
                
                if self.recv_video.is_broken() == True:
                    self.msg_send_to_ui["connection"]["video"] = False
                else:
                    self.msg_send_to_ui["connection"]["video"] = True
                
                if self.send_cmd.is_broken() == True:
                    self.msg_send_to_ui["connection"]["cmd"] = False
                else:
                    self.msg_send_to_ui["connection"]["cmd"] = True

    
    def listen_ui_else_msg(self):
        while self.all_serve:
            else_msg = self.msg_recv_from_ui["else"]
            if else_msg == "reconnect":
                self._reconnect()
            if else_msg == "exit":
                del(self)

    def _reconnect(self):
        self.communication_serve = False
        sleep(0.1)
        self.connect_to_server_and_start_service()
        self.communication_serve = True
            
    def __del__(self):
        self.all_serve = False
        sleep(0.2)

        del(self.recv_data)
        del(self.recv_video)
        del(self.send_cmd)

        del(self.ui)


if __name__ == "__main__":
    main_program = Main()
    main_program.start_ui_and_check()
    main_program.connect_to_server_and_start_service()
    main_program.start_main_function()