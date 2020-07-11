import communication.socket_comm as sc
import socket
import threading
from multiprocessing import Process
from video.frame_grabber import FrameGrabber
import time


def odo_in(odo_port=8000):
    client = sc.Socket()
    connected = False
    while not connected:
        try:
            client.connect(socket.gethostname(), odo_port)
            connected = True
        except ConnectionRefusedError:
            print(f"Connection on port {odo_port} refused. Retry in 5 sec.")
            time.sleep(5)
    listener_thread = threading.Thread(target=client.recv_stream)
    listener_thread.start()
    while True:
        client.wait()
        received_data = client.get_msg_data()
        print(received_data)


def video_out(ip_address='127.0.0.1', video_port=8008):
    camera = FrameGrabber()
    camera.connect_device()
    camera.connect_to_remote(ip_address=ip_address,
                             port=video_port, action='send')
    capture_thread = threading.Thread(target=camera.capture_video_stream)
    # capture_thread.daemon = True
    capture_thread.start()
    camera.stream_out()


def main():
    odomentry_proc = Process(target=odo_in, daemon=True)
    video_proc = Process(target=video_out, daemon=True)
    odomentry_proc.start()
    video_proc.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(100)
