from control.js_linux import Joystick
from control.odometry_control import OdoControl
import threading
import communication.socket_comm as sc
import socket

def main():
	# set up the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 8001
	print(port)
	s.bind(('', port))
	s.listen(1)
	clientsocket, address = s.accept()
	server = sc.Socket(clientsocket)

	motor_control = OdoControl(run_method=server.send)
	js_events = Joystick()
	motor_control_thread = threading.Thread(target=motor_control.send_joystick_control, args=(js_events,))
	js_events_thread = threading.Thread(target=js_events.listen)
	motor_control_thread.start()
	js_events_thread.start()

if __name__ == '__main__':
	main()
