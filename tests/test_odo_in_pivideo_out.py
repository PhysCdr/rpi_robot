import communication.socket_comm as sc
import socket
import threading
from multiprocessing import Process
from video.frame_grabberPI import FrameGrabberPI
import time


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
    listener_thread.start()
    while True:
        client.wait()
        received_data = client.get_msg_data()
        print(received_data)


def video_out(ip_address='127.0.0.1', video_port=8008):
    camera = FrameGrabberPI()
    camera.connect_device(resolution=(320,240))
    camera.connect_to_remote(ip_address=ip_address,
                             port=video_port, action='send')
    capture_thread = threading.Thread(target=camera.capture_video_stream)
    # capture_thread.daemon = True
    capture_thread.start()
    camera.stream_out()


def main():
    odomentry_proc = Process(target=odo_in, args=('192.168.x_server.xx_server', 8008), daemon=True)
    video_proc = Process(target=video_out, args=('192.168.x_pi.xx_pi', 8000), daemon=True)
    odomentry_proc.start()
    video_proc.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
