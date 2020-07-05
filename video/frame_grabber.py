import numpy as np
import cv2 as cv
from threading import Event
import imagezmq
import socket

class FrameGrabber(Event):
    def __init__(self):
        super().__init__()
        self.clear()
        self.frame = None
        self.cap =  None # capture device
        self.sender = None
        self.receiver = None
        self.hostname = socket.gethostname()

    def connect_device(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError('Cannot open camera')
    
    def connect_to_remote(self, ip_address, port, action='send'):
        """Connects to a remote machine to either send or receive messages"""
        if action == 'send':
            self.sender = imagezmq.ImageSender(connect_to=f"tcp://{ip_address}:{port}", REQ_REP=False)
        elif action == 'receive':
            self.receiver = imagezmq.ImageHub(open_port=f"tcp://{ip_address}:{port}", REQ_REP = False)

    def stream_out(self):
        while True:
            # read the frame from the camera and send it to the server
            self.wait()
            self.sender.send_image(self.hostname, self.frame)

    def stream_in(self, viewer=False):
        while True:
            self.clear()
            _, self.frame = self.receiver.recv_image()
            self.set()
            if viewer:
                self.show_frame()

    def capture_video_stream(self, viewer=False):
        while True:
            # Capture frame-by-frame
            ret, self.frame = self.cap.read()
            # if frame is read correctly ret is True
            self.set()
            if not ret:
                raise RuntimeError("Cannot receive frame (stream end?). Exiting ...")

            if viewer:
                self.show_frame()

            self.clear()
            if cv.waitKey(1) == ord('q'):
                break

    def get_frame(self):
        return self.frame

    def show_frame(self, frame=None):
        if frame is None:
            frame = self.frame
        # Display the resulting frame
        cv.imshow('frame', frame)
        cv.waitKey(1)
    
    def disconnect():
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()
        