import RPi.GPIO as GPIO
import time

#GPIO SETUP
PIN = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)


print("Door Sensor Test. Use ctrl +c to stop")
time.sleep(2)
print("Ready")

try:
    # infinite loop
    while True:
            if GPIO.input(PIN):
                print("Door is OPENED")
                time.sleep(1)
            else:
                print("Door is CLOSES")
                time.sleep(1);

except KeyboardInterrupt:
                print("Quit")
                GPIO.cleanup()
