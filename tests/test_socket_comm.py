import communication.socket_comm as sc
import socket
import threading
import random

client = sc.Socket()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8005
s.bind((socket.gethostname(), port))
s.listen(1)
client.connect(socket.gethostname(), port)
clientsocket, address = s.accept()
server = sc.Socket(clientsocket)
t1 = threading.Thread(target=client.recv_stream)
t1.daemon = True
t1.start()
test_data = []
for i in range(10):
	test_data.append(random.random())
	server.send(test_data)
	client.wait(0.01)
	received_data = client.get_msg_data()
	print(received_data)
print('done')
