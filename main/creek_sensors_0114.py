
import subprocess
import sys
import time

import Adafruit_ADS1x15
import RPi.GPIO as GPIO

# General Setting
SLEEP_TIME = 30 * 60

# RainSensor Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)

# TemperatureSensor Setting
SENSOR_ID = "28-01191ed4dcbc"
SENSOR_W1_SLAVE = "/sys/bus/w1/devices/" + SENSOR_ID + "/w1_slave"
ERR_VAL = 85000

# DO,pH Setting
ADC = Adafruit_ADS1x15.ADS1115()
GAIN = 1
REPE_NUM = 100
REPE_TIME = 0.2

PH_MID = 25200
PH_SLOPE_LOW = 1192
PH_INTERCEPT_LOW = 17177
PH_SLOPE_HIGH = 1626
PH_INTERCEPT_HIGH = 14257

DO_SLOPE = -474
DO_INTERCEPT = 1312

def ph_calc(value):
    if value < PH_MID:
        ph = (value - PH_INTERCEPT_LOW) / PH_SLOPE_LOW
    else:
        ph = (value - PH_INTERCEPT_HIGH) / PH_SLOPE_HIGH
    return ph

def do_calc(value):
    do = (value - DO_INTERCEPT) / DO_SLOPE
    return do

def main():
    while True:
        weather = get_rain_state()
        temp = get_temp_value()
        do, ph = get_DoPh_value()

        time.sleep()

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

def get_DoPh_value():
    try:
        do_sum = 0
        ph_sum = 0
        for _ in range(REPE_NUM):
            do_sum += ADC.read_adc(0, gain=GAIN)
            ph_sum += ADC.read_adc(1, gain=GAIN)
            time.sleep(REPE_TIME)

        do_value = do_sum/REPE_NUM
        ph_value = ph_sum/REPE_NUM
        do = do_calc(do_value)
        ph = ph_calc(ph_value)
        return ph, do
    except:
        return None

if __name__ == '__main__':
    main()