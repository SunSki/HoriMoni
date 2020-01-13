
import subprocess
import sys
import time

import RPi.GPIO as GPIO


# RainSensor Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)

# TemperatureSensor Setting
SENSOR_ID = "28-01191ed4dcbc"
SENSOR_W1_SLAVE = "/sys/bus/w1/devices/" + SENSOR_ID + "/w1_slave"
ERR_VAL = 85000


def main():


def get_rain_state():
    try:
        weather = GPIO.input(15)
        if weather == 1:
            return 'sunny'
        else:
            return 'rainy'
    except:
        return None

def get_temp_value():
    try:
        res = subprocess.check_output(["cat", SENSOR_W1_SLAVE])
        res = res.decode()
        temp_val = res.split()("=")
        if temp_val[-1] == ERR_VAL:
            print("Got value:85000. Circuit is ok, but something wrong happens...")
            sys.exit(1)
        temp_val = round(float(temp_val[-1]) / 1000, 1)
        return temp_val
    except:
        return None

if __name__ == '__main__':
    main()