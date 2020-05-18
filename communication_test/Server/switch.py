'''
    Created by Eric
    on Apr.05.2020
'''

from socket import *
from threading import Thread
from time import sleep

class Switch:
    '''
        Class of a data switcher
    '''
    def __init__(self, ip, port_recv, port_send, max_recv):
        '''
            ip: str, ip address of the machine
            port_recv: int, port which data comein by
            port_send: int, port which data send out by
            max_recv: int, size of the binary sent
        '''
        
        self.serve = True

        self.max_recv = max_recv
        self.conn_no = 0
        self.conn_recv = None
        self.conn_send = None

        self.socket_recv = socket(AF_INET, SOCK_STREAM)
        self.socket_recv.bind((ip, port_recv))
        self.socket_recv.listen(10)

        self.socket_send = socket(AF_INET, SOCK_STREAM)
        self.socket_send.bind((ip, port_send))
        self.socket_send.listen(10)

    def run(self):
        t_service = Thread(target = self._service, args = ())
        t_service.start()

    def _service(self):
        broken = False
        t_conn_recv = Thread(target = self._connect_recv, args = ())
        t_conn_send = Thread(target = self._connect_send, args = ())
        t_conn_recv.start()
        t_conn_send.start()
        print("LISTEN")
        while self.conn_no != 2:
            sleep(0.1)
        
        while self.serve:
            print("SERVE")
            try:
                data = self.conn_recv.recv(self.max_recv)
            except:
                self.conn_no -= 1
                t_conn_recv = Thread(target = self._connect_recv, args = ())
                t_conn_recv.start()
            print(data)
            try:
                self.conn_send.send(data)
            except:
                self.conn_no -= 1
                t_conn_send = Thread(target = self._connect_send, args = ())
                t_conn_send.start()

    def _connect_recv(self):
        self.conn_recv, addr = self.socket_recv.accept()
        print("RECV_CONN!")
        self.conn_no += 1

    def _connect_send(self):
        self.conn_send, addr = self.socket_send.accept()
        print("SEND_CONN!")
        self.conn_no += 1

    def __del__(self):
        self.serve = False
        sleep(0.1)
        self.socket_recv.close()
        self.socket_send.close()