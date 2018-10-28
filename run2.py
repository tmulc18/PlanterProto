import RPi.GPIO as GPIO
import serial
import time
import datetime
from utils import *
import Logger


# === CONFIG VARIABLES ===
WATER_PUMP_PIN = 20
MAIN_LIGHT_PIN = 21

# State Variables
water_pump_pin_s = None
main_light_pin_s = None

# Preference variables
LIGHT_START_HOUR = 4
LIGHT_START_MIN = 0
LIGHT_START_SEC = 0

TIME_LIGHT = 8*60 # seconds per day

SECONDS_PER_DAY = 24*60*60 # total seconds in day

LOOP_LAG = 1 # seconds between checks in states

ARDUINO_BAUD = 9600
SERIAL_ADDRESS = '/dev/ttyAMA0'

# === SETUP PINS AND STATES ===

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

# Setup pins
GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
GPIO.setup(MAIN_LIGHT_PIN, GPIO.OUT) 

# start time in seconds
start_time = time.time()

# start serial for input
ser = serial.Serial(SERIAL_ADDRESS, ARDUINO_BAUD, timeout=1)

# initialize Logger
logger = Logger.Logger()


# === MAIN LOOP ===
while(True):
    current_time = time.time()
    duration = current_time - start_time
    
    # serial
    arduino_mes = ser.readline()
    print(arduino_mes)

    # controls lights
    if duration%SECONDS_PER_DAY < TIME_LIGHT:
        main_light_pin_s = 1
        GPIO.output(MAIN_LIGHT_PIN,1)
    else:
        main_light_pin_s = 0
    GPIO.output(MAIN_LIGHT_PIN,
                    main_light_pin_s)

    # logging
    logger.parseInput(arduino_mes)
    logger.log()

    # log ph
    # ...

    # log co2
    # ...

    # log lights
    # ...
    # log_lights(main_light_pin_s)

    # loop lag for pi health
    time.sleep(LOOP_LAG)
