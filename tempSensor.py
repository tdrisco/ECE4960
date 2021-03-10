import adafruit_dht
import time

from board import *

DHT_PIN = D4;
DHT_SENSOR = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)


while True:

    humidity = DHT_SENSOR.humidity
    temperature = DHT_SENSOR.temperature
    
    print("Temp={0:0.1f}C   Humidity={1:0.1f}%".format(temperature, humidity));

    time.sleep(3);
