import subprocess
import cv2


class FrameGrabberPI(Event):
    """docstring for FrameGrabberPI"""

    def __init__(self, target_ip, target_port, resolution=(640, 480),
                 bitrate=2000000, fps=30, capture_time='capture_continuous'):
        super().__init__()
        self.target_address = f"udp://{target_ip}:{target_port}"
        self.frame_width = resolution[0]
        self.frame_height = resolution[1]
        self.bitrate = int(bitrate)
        self.fps = fps
        if capture_time == 'continuous':
            self.capture_time = 0
        else:
            self.capture_time = capture_time
        self.capture_process = None
        self.capture_cv2 = None

    def __restart_device(self):
        try:
            self.capture_process.terminate()
            self.connect_device()
        except AttributeError:
            pass

    def stop_device(self):
        try:
            self.capture_process.terminate()
        except AttributeError:
            pass

    def set_resolution(self, resolution):
        self.frame_width = resolution[0]
        self.frame_height = resolution[1]
        self.__restart_device()

    def get_resolution(self):
        return (self.frame_width, self.frame_height)

    def set_bitrate(self, bitrate):
        self.bitrate = int(bitrate)
        self.__restart_device()

    def get_bitrate(self):
        return self.bitrate

    def set_fps(self, fps):
        self.fps = fps
        self.__restart_device()

    def get_fps(self):
        return self.fps

    def set_target_address(self, target_ip, target_port):
        self.target_address = f"udp://{target_ip}:{target_port}"
        self.__restart_device()

    def set_capture_time(self, capture_time):
        if capture_time == 'continuous':
            self.capture_time = 0
        else:
            self.capture_time = capture_time
        self.__restart_device()

    def get_target_address(self):
        target_address = self.target_address.split(':')
        target_port = target_address[-1]
        target_ip = target_address[1].split('//')[-1]
        return target_ip, int(target_port)

    def connect_device(self):
        # initialize the camera and grab a reference to the raw camera capture
        # raspivid -t 0 -w 320 -h 240 -b 4000000 -fps 30 -cd MJPEG -o udp://192.168.x.xx:8000
        self.capture_process = subprocess.Popen(['raspivid', '-t', self.capture_time,
                                                 '-w', self.frame_width, '-h', self.frame_height,
                                                 '-b', self.bitrate, '-fps', self.fps, '-cd', 'MJPEG',
                                                 '-o', self.target_address])

    def connect_to_remote(self):
        self.capture_cv2 = cv2.VideoCapture(
            self.target_address, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            print('VideoCapture not opened')
            exit(-1)

    def capture_video_stream(self, viewer=True):
        if self.capture_cv2:

            while True:
                ret, frame = self.capture_cv2.read()
                self.set()

                if not ret:
                    print('frame empty')
                    break

                if viewer:
                    cv2.imshow('image', frame)

                if cv2.waitKey(1) & 0XFF == ord('q'):
                    break
                self.clear()

            cap.release()
            self.disconnect()

    def disconnect():
        self.stop_device()
        # When everything done, release the capture
        cv2.destroyAllWindows()
