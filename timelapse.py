import argparse
import time
from picamera import PiCamera


def main(interval, duration, fname='pic_'):
	"""Takes photo every inteval minutes 
	for duration many hours."""

	camera = PiCamera()
	camera.resolution = (1024, 768)

	num_photos = (duration*60.0)/interval
	for i in range(num_photos):
		camera.capture(fname+str(i)+'.jpg')
		time.sleep(interval*60) #wait for the next photo


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-interval', default = 5
						help='number of minutes between photos')
	parser.add_argument('-duration', default = 24
						help='number of hours of timelapse')

	param_dict = vars(parser.parse_args())

	interval = param_dict['interval']
	duration = param_dict['duration']

	main(interval, duration)