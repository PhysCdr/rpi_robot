from control.js_linux import Joystick
from control.odometry_control import OdoControl
import threading
import communication.socket_comm as sc
import socket
import cv2 as cv
from video.frame_grabber import FrameGrabber
from multiprocessing import Process
import time


def odo_out(odo_port=8000):
    # set up the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', odo_port))
    s.listen(1)
    clientsocket, address = s.accept()
    server = sc.Socket(clientsocket)

    motor_control = OdoControl(run_method=server.send)
    js_events = Joystick()
    motor_control_thread = threading.Thread(
        target=motor_control.send_joystick_control, args=(js_events,))
    js_events_thread = threading.Thread(target=js_events.listen)
    motor_control_thread.start()
    js_events_thread.start()


def video_in(ip_address='127.0.0.1', video_port=8008):
    camera = FrameGrabber()
    camera.connect_to_remote(ip_address=ip_address,
                             port=video_port, action='receive')
    camera.stream_in(viewer=True)


def main():
    odomentry_proc = Process(target=odo_out, args=(8008,), daemon=True)
    video_proc = Process(target=video_in, args=('192.168.0.9', 8000), daemon=True)
    odomentry_proc.start()
    video_proc.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
