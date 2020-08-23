from control.js_linux import Joystick
from control.odometry_control import OdoControl
import threading

def main():

	motor_control = OdoControl()
	js_events = Joystick()
	# motor_control_thread = threading.Thread(target=motor_control.send_joystick_control, args=(js_events,))
	js_events_thread = threading.Thread(target=js_events.listen)
	# motor_control_thread.start()
	js_events_thread.start()
	# js_events.listen()
	print('domn')
	while True:	
		js_events.wait()
		motor_control.js_axis_to_lr_speeds(js_events)

if __name__ == '__main__':
	main()