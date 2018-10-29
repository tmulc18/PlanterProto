import argparse
import time
from picamera import PiCamera


def main(interval, duration, dir_='photos', fname='pic_'):
	"""Takes photo every inteval minutes 
	for duration many hours."""

	camera = PiCamera()
	camera.resolution = (1024, 768)

	num_photos = (duration*60.0)/interval
	for i in range(num_photos):
		camera.capture(dir_+'/'+fname+str(i)+'.jpg')
		time.sleep(interval*60) #wait for the next photo


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-interval', default = 5
						help='number of minutes between photos')
	parser.add_argument('-duration', default = 24
						help='number of hours of timelapse')
	parser.add_argument('-dir', default = 'timelapse_photos'
						help='folder to store timelapse')

	param_dict = vars(parser.parse_args())

	interval = param_dict['interval']
	duration = param_dict['duration']
	dir_ = param_dict['dir']

	main(interval, duration, dir_)