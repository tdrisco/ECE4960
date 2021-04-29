import RPi.GPIO as GPIO
import time

#GPIO SETUP
PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)


def NOISE(PIN):
        #if GPIO.input(PIN):
        print("Sound Detected!")
        #else:
                #print("Sound Detected!")

print("Sound Sensor Test. Use ctrl +c to stop")
time.sleep(2)
print("Ready")

try:

    GPIO.add_event_detect(PIN, GPIO.BOTH, bouncetime=300, callback=NOISE)  # let us know when the pin goes HIGH or LOW

    # infinite loop
    while True:
            time.sleep(1)

except KeyboardInterrupt:
                print("Quit")
                GPIO.cleanup()
