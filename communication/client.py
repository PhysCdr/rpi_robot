import socket
HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8000))

full_msg = ''
new_msg = True
while True:
	msg = s.recv(16)
	if new_msg:
		print(f"new message length: {msg[:HEADERSIZE]}")
		msg_len = int(msg[:HEADERSIZE])
		new_msg = False
	full_msg += msg.decode()

	if len(full_msg) - HEADERSIZE == msg_len:
		new_msg = True
		print('full message recieved')
		print(full_msg)
		full_msg = ''


print(full_msg)