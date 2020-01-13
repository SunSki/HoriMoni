from time import sleep
import RPi.GPIO as GPIO

# RainSensor Setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)
RAIN_REPE_NUM = 100
RAIN_REPE_TIME = 0.2

def get_rain_state():
    for _ in range(RAIN_REPE_NUM):
        weather = GPIO.input(15)
        if weather == 0:
            return 'rainy'
        sleep(RAIN_REPE_TIME)
    return 'sunny'

def main():
    print("Start checking...")
    weather = get_rain_state()
    print(weather)


if __name__ == "__main__":
    main()