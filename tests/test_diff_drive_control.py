import communication.socket_comm as sc
import socket
import threading
from control.diff_drive import DiffDrive
from control.odometry_control import OdoControl

client = sc.Socket()
port = 8001
client.connect('192.168.0.9', port)
listener_thread = threading.Thread(target=client.recv_stream)
odometry_control = OdoControl(run_method=client.get_msg_data)
odometry_control_thread = threading.Thread(target=odometry_control.receive_control, args=(client,))
listener_thread.daemon = True
odometry_control_thread.daemon = True
listener_thread.start()
odometry_control_thread.start()
left = (7,8)
right = (9,10)
diff_drive = DiffDrive(left, right)

while  True:
	odometry_control.wait()
	diff_drive.go(*odometry_control.get_speeds())

# motor_control = OdoControl(run_method=server.send)
# js_events = Joystick()
# motor_control_thread = threading.Thread(target=motor_control.send_joystick_control, args=(js_events,))
# js_events_thread = threading.Thread(target=js_events.listen)
# motor_control_thread.start()
# js_events_thread.start()
