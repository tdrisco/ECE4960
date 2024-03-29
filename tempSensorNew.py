import adafruit_dht

DHT_PIN = 17;
DHT_SENSOR = Adafruit_DHT.DHT22




while True:

    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not none and temperature is not None:
        print("Temp={0:0.1f}C   Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor Failed, was not able to retrieve data")

