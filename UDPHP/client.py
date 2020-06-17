"""
    Connect to server
    Wait for peer's addr
    Close socket
    New socket
    Send to peer's addr
"""

from socket import *
from time import sleep
from threading import Thread

SERVER_ADDR = ("45.249.94.168", 1234)
S = socket(AF_INET, SOCK_DGRAM)
S.sendto(b"hi", SERVER_ADDR)
recv = S.recv(1024)
print("recv: ", recv)
# S.close()

SELF_ADDR = (
    eval(recv.decode())[0][0],
    # "",
    eval(recv.decode())[0][1]
)

PEER_ADDR = (
    eval(recv.decode())[1][0],
    eval(recv.decode())[1][1]
)

def sending(S):
    while True:
        S.sendto(b"hello", PEER_ADDR)
        print("send")
        sleep(0.5)

def recving(S):
    while True:
        recv = S.recvfrom(1024)
        print("recv", recv)

Ts = Thread(target = sending, args = (S,))
Tr = Thread(target = recving, args = (S,))
Ts.start()
Tr.start()
