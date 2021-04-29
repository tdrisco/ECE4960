import adafruit_dht
import time

from board import *

DHT_PIN = D17;
DHT_SENSOR = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)

while True:

    temperature = DHT_SENSOR.temperature
    humidity = DHT_SENSOR.humidity
    
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C   Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor Failed, was not able to retrieve data")
    
    time.sleep(5)

