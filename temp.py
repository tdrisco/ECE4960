
import time
#import board
import adafruit_dht

import RPi.GPIO as GPIO

# Initial the dht device, with data pin connected to:
GPIO.setmode(GPIO.BCM)
DHT_PIN = 17
GPIO.setup(DHT_PIN, GPIO.IN)

dhtDevice = adafruit_dht.DHT22(DHT_PIN)

print("Temperature Sensor test. Use ctrl +c to stop")
time.sleep(2)
print("Ready\n")

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature #get temperature value
        temperature_f = temperature_c * (9 / 5) + 32 #convert to farenhiet
        humidity = dhtDevice.humidity #get humidity value
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

    except KeyboardInterrupt:
                    print("Quit")
                    GPIO.cleanup()
    except RuntimeError as error: #How to handle inevitable errors
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error


    time.sleep(2.0)
