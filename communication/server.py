import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8000))
s.listen(1 )

while True:
	clientsocket, address = s.accept()
	print('Connection to {} established'.format(address))
	msg = str(address)
	msg = f'{len(msg) :< {HEADERSIZE}}' + msg
	clientsocket.send(msg.encode())