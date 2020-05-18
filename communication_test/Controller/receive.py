from socket import *
from threading import Thread
from time import sleep

class Receive:
    def __init__(self):
        self.serve = True
        self.data = None

        self.my_socket = socket(AF_INET, SOCK_STREAM)
        self.broken = None
    
    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        try:
            self.my_socket.connect((ip, port))
            self.broken = False
            return 1
        except:
            return 0

    def run(self, MAX_RECV):
        t = Thread(target = self._service, args = (MAX_RECV,))
        t.start()

    def _service(self, MAX_RECV):
        while self.serve:
            try:
                self.data = self.my_socket.recv(MAX_RECV)
                self.broken = False
            except:
                self.broken = True
                self.connect(self.ip, self.port)

    def get_data(self):
        return self.data

    def is_broken(self):
        return self.broken

    def __del__(self):
        self.serve = False
        sleep(0.1)
        self.my_socket.close()