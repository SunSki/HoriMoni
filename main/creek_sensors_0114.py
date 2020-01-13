import RPi.GPIO as GPIO
import time

# RainSensor Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)

