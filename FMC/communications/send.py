'''
    Created by Eric
    on Apr.11.2020

    socket send module
'''

from socket import *
from threading import Thread
from time import sleep

class Send:
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

    def run(self, delay):
        t = Thread(target = self._service, args = (delay,))
        t.start()

    def _service(self, delay):
        while self.serve:
            try:
                self.my_socket.send(self.data)
                self.broken = False
            except:
                self.broken = True
                self.connect(self.ip, self.port)
                
                
            sleep(delay)

    def change_data(self, new_data):
        self.data = new_data

    def is_broken(self):
        return self.broken

    def __del__(self):
        self.serve = False
        sleep(0.1)
        self.my_socket.close()