import RPi.GPIO as GPIO
import time
import datetime
from utils import *

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

WATER_PUMP_PIN = 20
MAIN_LIGHT_PIN = 21

# State Variables
water_pump_pin_s = None
main_light_pin_s = None

# Preference variables
LIGHT_START_HOUR = 4
LIGHT_START_MIN = 0
LIGHT_START_SEC = 0


#TIME_WATER = 5 # seconds per day
TIME_LIGHT = 8*60 # seconds per day

SECONDS_PER_DAY = 24*60*60 # total seconds in day

LOOP_LAG = 1 # seconds between checks in states

# Setup pins
GPIO.setup(WATER_PIN, GPIO.OUT)  # set up pin 17
GPIO.setup(LIGHT_PIN, GPIO.OUT)  # set up pin 18

# start time in seconds
start_time = time.time()

while(True):
  current_time = time.time()
  duration = current_time - start_time
  #if duration%SECONDS_PER_DAY < TIME_WATER:
  #  GPIO.output(WATER_PIN,1)
  #else:
  #  GPIO.output(WATER_PIN,0)

  # controls lights
  if duration%SECONDS_PER_DAY < TIME_LIGHT:
    main_light_pin_s = 1
    GPIO.output(LIGHT_PIN,1)
  else:
    main_light_pin_s = 0
  GPIO.output(LIGHT_PIN,
          main_light_pin_s)

  # control pump
  # ...

  # log EC
  # ...

  # log temp
  # ...

  # log ph
  # ...

  # log co2
  # ...

  # log lights
  # ...
  # log_lights(main_light_pin_s)

  # loop lag for pi health
  time.sleep(LOOP_LAG)
