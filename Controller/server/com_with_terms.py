from socket import *
import struct
import global_var

class communicateWithTerminals:
    
    LOCAL_SERVER_IP = "169.1.1.1"

    CONN_SOCK_PORT = 1234
    PFD_SOCK_PORT = 2345
    """
        Use TCP Protocol

             --------------
            | Local Server | <- RPi
    data -> |              | <- PAP
   video -> |              | -> PFD
 command <- |              | <- ECAM_I
             --------------  -> ECAM_O
    

    Server process:
        New 5 threads -> listen for conn
        -> Recv conn -> recv id -> process according to id

        IF conn crash -> re-listen for conn
    """

    def __init__(self):
        self.terminal_role_addr_table = {}

        self.conn_sock = socket(AF_INET, SOCK_DGRAM)
        self.conn_sock.bind((self.LOCAL_SERVER_IP, self.CONN_SOCK_PORT))

        self.pfd_sock = socket(AF_INET, SOCK_DGRAM)
        self.pfd_sock.bind((self.LOCAL_SERVER_IP, self.PFD_SOCK_PORT))


    def run(self):
        pass

    def _pfd_send(self):
        while True:
            packed_data = struct.pack("", 
                global_var.data_list["PITCH"],
                global_var.data_list["ROLL"],

                global_var.data_list["AIR_V"],
                global_var.data_list["GROUND_V"],
                global_var.data_list["ACCEL"],

                global_var.data_list["ALT"],
                global_var.data_list["RADIO_H"],
                global_var.data_list["VS"],

                global_var.data_list["HDG"],

                global_var.data_list["LONG"],
                global_var.data_list["LAT"],

                global_var.local_infos["FD_ON"],

                global_var.local_infos["TAR_SPEED"],
                global_var.local_infos["TAR_ALT"],
                global_var.local_infos["TAR_HDG"],
                global_var.local_infos["TAR_LONG"],
                global_var.local_infos["TAR_LAT"],

                *list(global_var.local_infos["STATUS"].values())
            )

            for addr in self.terminal_role_addr_table["pfd"]:
                self.pfd_sock.sendto(packed_data, addr)

    def _listen_conn(self):
        while True:
            try:
                content, addr = self.conn_sock.recvfrom(1024)
                if content.decode() in self.terminal_role_addr_table:
                    if addr not in self.terminal_role_addr_table[content.decode()]:
                        self.terminal_role_addr_table[content.decode()].append(addr)
                else:
                    self.terminal_role_addr_table.update({content.decode(): [addr]})
            except:
                pass