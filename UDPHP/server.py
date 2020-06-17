"""
    Wait for 2 connection
    send addr of each to another
    done
"""

from socket import *

SERVER_ADDR = ("45.249.94.168", 1234)
S = socket(AF_INET, SOCK_DGRAM)
S.bind(SERVER_ADDR)

x_0, addr_0 = S.recvfrom(1024)
print("addr_0: ", addr_0)

x_1, addr_1 = S.recvfrom(1024)
print("addr_1: ", addr_1)

S.sendto(str([addr_0, addr_1]).encode(), addr_0)
S.sendto(str([addr_1, addr_0]).encode(), addr_1)

S.close()
