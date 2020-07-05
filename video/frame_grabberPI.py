# import the necessary packages
from frame_grabber import FrameGrabber
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class FrameGrabberPI(FrameGrabber):
	"""docstring for FrameGrabberPI"""
	def __init__(self):
		super().__init__()
		self.rawCapture = None

	def connect_device(self, resolution=(640, 480), framerate=32):
		# initialize the camera and grab a reference to the raw camera capture
		self.cap = PiCamera()
		self.cap.resolution = resolution
		self.cap.framerate = framerate
		self.rawCapture = PiRGBArray(self.cap, size=(640, 480))
		# allow the camera to warmup
		time.sleep(0.1)

	def capure_video_stream(self):
	# capture frames from the camera
	for frame in self.cap.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		self.frame = frame.array
		self.set()
		key = cv2.waitKey(1) & 0xFF
		# clear the stream in preparation for the next frame
		self.rawCapture.truncate(0)
		# if the `q` key was pressed, break from the loop
		self.clear()
		if key == ord("q"):
			break

	def disconnect():
        # When everything done, release the capture
        cv.destroyAllWindows()