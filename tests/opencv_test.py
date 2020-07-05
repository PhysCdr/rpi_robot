from video.frame_grabber import FrameGrabber
import threading

# set up the server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8002
# s.bind((socket.gethostname(), port))
# s.listen(1)
# clientsocket, address = s.accept()
# server = sc.Socket(clientsocket)

camera = FrameGrabber()
camera.connect_device()
camera.connect_to_remote(ip_address='127.0.0.1' , port=port, action='send')
capture_thread = threading.Thread(target=camera.capture_video_stream)
capture_thread.daemon = True
capture_thread.start()
camera.stream_out()
