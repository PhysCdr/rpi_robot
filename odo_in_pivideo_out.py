import communication.socket_comm as sc
from control.diff_drive import DiffDrive
from control.odometry_control import OdoControl
import socket
import threading
from multiprocessing import Process
from video.frame_grabberPI import FrameGrabberPI
import time
import subprocess


def odo_in(ip_address, odo_port=8000):
    client = sc.Socket()
    connected = False
    while not connected:
        try:
            client.connect(ip_address, odo_port)
            connected = True
        except ConnectionRefusedError:
            print("Connection on port {} refused. Retry in 5 sec.".format(odo_port))
            time.sleep(5)
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


def video_out(ip_address='127.0.0.1', video_port=8008,
	          resolution=(320, 240), bandwidth=4000000, fps=30):
	video_stream = ['raspivid', '-t', '0', '-w', str(resolution[0]),
	                '-h', str(resolution[1]), '-b', str(bandwidth),
	                '-fps', str(fps), '-cd', 'MJPEG',
	                '-o', 'udp://{}:{}'.format(ip_address, video_port)]
	subprocess.run(video_stream)
    # raspivid -t 0 -w 320 -h 240 -b 4000000 -fps 30 -cd MJPEG -o udp://192.168.x.xx:8000


def main():
	ip_remote = '192.168.xx.xx'
    odomentry_proc = Process(target=odo_in, args=(ip_remote, 8008), daemon=True)
    video_proc = Process(target=video_out, args=(ip_remote, 8000), daemon=True)
    odomentry_proc.start()
    video_proc.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
