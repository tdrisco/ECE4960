import RPi.GPIO as GPIO
import time

#GPIO SETUP
PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)


#def LIGHT(PIN):
        #print("Light On")

print("Light Sensor Test. Use ctrl +c to stop")
time.sleep(2)
print("Ready")

try:

    #GPIO.add_event_detect(PIN, GPIO.RISING, callback=LIGHT)  # let us know when the pin goes HIGH or LOW
    # infinite loop
    while True:
            if GPIO.input(PIN):
                print("Light On \u263e")
                time.sleep(1)
            else:
                print("Light Off \u263c")
                time.sleep(1);

except KeyboardInterrupt:
                print("Quit")
                GPIO.cleanup()
