# Communicate with local server

from socket import *

SERVER_ADDR = ("192.168.114.514", 1234)

class Communicate:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(SERVER_ADDR)

    def send(self, data):
        self.sock.send(data)

    def recv(self):
        return self.sock.recv(1024)