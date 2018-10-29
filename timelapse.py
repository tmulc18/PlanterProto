import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import scipy.misc



def main(fname='pic_',interval=5):
	"""Takes photo every inteval minutes."""

	camera = piCamera()
	camera.resolution = (1024, 768)
	camera.capture(fname+'.jpg')
	time.sleep(interval*1) #wait for the next photo

	

if __name__ == "__main__":
	main()