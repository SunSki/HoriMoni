#!/path/to/python
# -*- coding: utf-8 -*-
import Adafruit_ADS1x15
import time

CHANNEL = 0
GAIN = 1

adc = Adafruit_ADS1x15.ADS1115()

while True:
    print(adc.read_adc(CHANNEL, gain=GAIN))
    time.sleep(0.5)
