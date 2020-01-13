
import csv
from datetime import datetime
import json
import subprocess
import sys
from time import sleep

import Adafruit_ADS1x15
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import RPi.GPIO as GPIO

# General Setting
SLEEP_TIME = 30 * 60
LOCATION = "test"
CSV_FILE = "data/creek_data.csv"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

DO_SLOPE = 474
DO_INTERCEPT = -1312

# gspread Setting
print("Start gspread setting...")
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Key/creeks-1574788873145-ecb1ac12ac88.json', SCOPE)
GC = gspread.authorize(CREDENTIALS)

SPREADSHEET_KEY = '18jf-W56QqMvjSUgvxBv76Hm3H-HEmgkUZTz-7_Qx1F8' # 共有設定したスプレッドシートキー
WORKSHEET = GC.open_by_key(SPREADSHEET_KEY).sheet1 # 共有設定したスプレッドシートのシート１を開く
print("Finish gspread setting")

def ph_calc(value):
    if value < PH_MID:
        ph = (value - PH_INTERCEPT_LOW) / PH_SLOPE_LOW
    else:
        ph = (value - PH_INTERCEPT_HIGH) / PH_SLOPE_HIGH
    return ph

def do_calc(value):
    do = (value - DO_INTERCEPT) / DO_SLOPE
    return do


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
        temp_val = res.split("=")
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
            sleep(REPE_TIME)

        do_value = do_sum/REPE_NUM
        ph_value = ph_sum/REPE_NUM
        do = do_calc(do_value)
        ph = ph_calc(ph_value)
        return do, ph
    except:
        return None, None

# weather, temp, do, ph
def get_data():
    print("Start Get data...")
    try:
        weather = get_rain_state()
        print("weather: {}".format(weather))
        temp = get_temp_value()
        print("temp: {}".format(temp))
        do, ph = get_DoPh_value()
        print("do: {}, ph: {}".format(do, ph))
        return weather, temp, do, ph
    except:
        return None

def write_csv(list):
    with open(CSV_FILE, 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(list)
    print("Finish writing csv")

def write_spreadsheet(data):
    index = 1
    while True:
        num = str(index)
        Acell = 'A' + num
        if not WORKSHEET.acell(Acell).value:
            break
        index += 1

    data_num = len(data)
    row_ids = list(LETTERS)
    for i in range(data_num):
        row_id = row_ids[i]
        cell = row_id + num
        WORKSHEET.update_acell(cell, data[i])
    print("Finish writing spreadsheet")

def main():
    while True:
        weather, temp, do, ph = get_data()
        dt = datetime.now().strftime('%Y/%m/%d/%H:%M')
        data = [dt, weather, temp, do, ph, LOCATION]
        
        write_csv(data)
        write_spreadsheet(data)

        print("Sleep {}s".format(SLEEP_TIME))
        sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()