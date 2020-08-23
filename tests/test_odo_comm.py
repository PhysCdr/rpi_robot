import communication.socket_comm as sc
import socket
import threading

client = sc.Socket()
port = 8001
print(port)
client.connect('192.168.xx.xx', port)
listener_thread = threading.Thread(target=client.recv_stream)
listener_thread.start()
while  True:
	client.wait()
	received_data = client.get_msg_data()
	print(received_data)

# motor_control = OdoControl(run_method=server.send)
# js_events = Joystick()
# motor_control_thread = threading.Thread(target=motor_control.send_joystick_control, args=(js_events,))
# js_events_thread = threading.Thread(target=js_events.listen)
# motor_control_thread.start()
# js_events_thread.start()
