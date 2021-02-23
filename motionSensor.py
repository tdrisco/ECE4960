import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

def MOTION(PIR_PIN):
    print("Motion detected!")

print("PIR test. Use ctrl +c to stop")
time.sleep(2)
print("Ready")
try:
               GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
               while 1:
                              time.sleep(100)
except KeyboardInterrupt:
                print("Quit")
                GPIO.cleanup()
