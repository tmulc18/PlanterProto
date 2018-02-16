import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

WATER_PIN = 20
LIGHT_PIN = 21

TIME_WATER = 5 # seconds per day
TIME_LIGHT = 8*60 # seconds per day
SECONDS_PER_DAY = 24*60*60 # total seconds in day

LOOP_LAG = 1 # seconds between checks in states

# Setup pins
GPIO.setup(WATER_PIN, GPIO.OUT)  # set up pin 17
GPIO.setup(LIGHT_PIN, GPIO.OUT)  # set up pin 18

start_time = time.time() # start time in seconds

while(True):
  current_time = time.time()
  duration = current_time - start_time
  if duration%SECONDS_PER_DAY < TIME_WATER:
    GPIO.output(WATER_PIN,1)
  else:
    GPIO.output(WATER_PIN,0)

  if duration%SECONDS_PER_DAY < TIME_LIGHT:
    GPIO.output(LIGHT_PIN,1)
  else:
    GPIO.output(LIGHT_PIN,0)

  time.sleep(LOOP_LAG)
