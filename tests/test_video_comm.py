from video.frame_grabber import FrameGrabber
import threading
import cv2 as cv

port = 8002
camera = FrameGrabber()
camera.connect_to_remote(ip_address='127.0.0.1' , port=port, action='receive')
camera.stream_in(viewer=True)
# streamin_thread = threading.Thread(target=camera.stream_in)
# streamin_thread.daemon = True
# streamin_thread.start()

# while True:
# 	camera.wait()
	# frame = camera.get_frame()
	# cv.imshow('frame', frame)
