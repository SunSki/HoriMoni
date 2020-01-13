import Adafruit_ADS1x15
from time import sleep

# DO,pH Setting
ADC = Adafruit_ADS1x15.ADS1115()
GAIN = 1
DOPH_REPE_NUM = 150
DOPH_REPE_TIME = 0.2

PH_MID = 25200
PH_SLOPE_LOW = 1192
PH_INTERCEPT_LOW = 17177
PH_SLOPE_HIGH = 1626
PH_INTERCEPT_HIGH = 14257

DO_SLOPE = 474
DO_INTERCEPT = -1312

def ph_calc(value):
    if value < PH_MID:
        ph = (value - PH_INTERCEPT_LOW) / PH_SLOPE_LOW
    else:
        ph = (value - PH_INTERCEPT_HIGH) / PH_SLOPE_HIGH
    return ph

def do_calc(value):
    do = (value - DO_INTERCEPT) / DO_SLOPE
    return do

def get_DoPh_value():
    do_sum = 0
    ph_sum = 0
    for _ in range(DOPH_REPE_NUM):
        do_sum += ADC.read_adc(0, gain=GAIN)
        ph_sum += ADC.read_adc(1, gain=GAIN)
        sleep(DOPH_REPE_TIME)

    do_value = do_sum/DOPH_REPE_NUM
    ph_value = ph_sum/DOPH_REPE_NUM
    print("DO_value: {}, pH_value: {}".format(do_value, ph_value))
    do = do_calc(do_value)
    ph = ph_calc(ph_value)
    print("DO: {}, pH: {}".format(do, ph))

def main():
    while True:
        get_DoPh_value()

if __name__ == "__main__":
    main()