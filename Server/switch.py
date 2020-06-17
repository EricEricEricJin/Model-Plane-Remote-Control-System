from socket import *
from threading import Thread

class Switch:

    """
        Threads:
            |
            |- heartBit: recv heart bit package, modify send_addr
            |
            |- transmit: recv, send to recv_addr
    """

    def __init__(self, IP, recv_port, send_port, hb_port, max_recv):
        self.heartBit_sock = socket(AF_INET, SOCK_DGRAM)
        self.recv_sock = socket(AF_INET, SOCK_DGRAM)
        self.send_sock = socket(AF_INET, SOCK_DGRAM)

        self.heartBit_sock.bind((IP, hb_port))
        self.recv_sock.bind((IP, recv_port))
        self.send_sock.bind((IP, send_port))

        self.send_addr = None
        self.max_recv = max_recv
        self.serve = True

    def run(self):
        t_transmit = Thread(target = self._transmit)
        t_heartBit = Thread(target = self._heartBit)
        t_transmit.start()
        t_heartBit.start()

    def _transmit(self):
        while self.serve:
            try:
                data = self.recv_sock.recv(self.max_recv)
                print("Data:", data)
                try:
                    import struct
                    print(struct.pack("?Hh?H?Hhhh?HH??", data))
                except:
                    pass
                print("Addr:", self.send_addr)
                self.send_sock.sendto(data, self.send_addr)
            except Exception as e:
                # print(e)
                pass


    def _heartBit(self):
        while self.serve:
            data, self.send_addr = self.heartBit_sock.recvfrom(1024)
            # print("Heartbit data:", data)
            print("Heartbit addr:", self.send_addr, "Heartbit addr:", data)

    def __del__(self):
        self.serve = False
        self.recv_sock.close()
        self.send_sock.close()
        self.heartBit_sock.close()
