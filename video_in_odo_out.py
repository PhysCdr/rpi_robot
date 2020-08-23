from control.js_linux import Joystick
from control.odometry_control import OdoControl
import threading
import communication.socket_comm as sc
import socket
import cv2
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
    cap = cv2.VideoCapture(f'udp://{ip_address}:{video_port}',cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print('VideoCapture not opened')
        exit(-1)

    while True:
        ret, frame = cap.read()

        if not ret:
            print('frame empty')
            break

        cv2.imshow('image', frame)

        if cv2.waitKey(1)&0XFF == ord('q'):
            break


def main():
    ip_address = '192.168.xx.xx' # ip address of this machine
    odomentry_proc = Process(target=odo_out, args=(8008,), daemon=True)
    video_proc = Process(target=video_in, args=(ip_address, 8000), daemon=True)
    odomentry_proc.start()
    video_proc.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
