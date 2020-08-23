import socket
from threading import Event
import pickle
import time

HEADERSIZE = 10

class Socket(Event):

    def __init__(self, sock=None):
        super().__init__()
        self.clear()
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.data=None # stores the latest received message

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data):
        msg = pickle.dumps(data)
        msg = '{:< {}}'.format(len(msg), HEADERSIZE).encode() + msg
        self.sock.sendall(msg)
            

    def recv_stream(self):
        full_msg = ''.encode()
        new_msg = True
        while True:
            msg = ''.encode()
            self.clear()
            if new_msg:
                for i in range(HEADERSIZE):
                    msg += self.sock.recv(1)
                msg_len = int(msg)
                new_msg = False
            else:
                for i in range(msg_len):
                    msg += self.sock.recv(1)
                self.data = pickle.loads(msg)
                self.set() # set a message received event to True
                new_msg = True
                full_msg = ''.encode()

    def get_msg_data(self):
        return self.data
