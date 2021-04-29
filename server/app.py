from flask import Flask, render_template, Response, request
import RPi.GPIO as GPIO
import adafruit_dht
import time
import spidev
from camera import Camera
import os

app = Flask(__name__)

os.system("pkill -f 'libgpiod_pulsein'")

camera = Camera()
camera.run()

GPIO.setmode(GPIO.BCM)
pin="3"
GPIO.setup(int(pin), GPIO.IN)

DHT_PIN = 3
GPIO.setup(DHT_PIN, GPIO.IN)
dhtDevice = adafruit_dht.DHT22(DHT_PIN)

# Light sensor
LIGHT_PIN = 4
GPIO.setup(LIGHT_PIN, GPIO.IN)

# Door sensor
DOOR_PIN = 2
GPIO.setup(DOOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Motion sensor
PIR_PIN =13
GPIO.setup(PIR_PIN, GPIO.IN)

MOTION_DETECTED = "0"
SOUND_DETECTED = "0"

# Flame sensor
FLAME_PIN = 16
GPIO.setup(FLAME_PIN, GPIO.IN)

# Water sensor
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 250000
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

ALARM_MODE = "Mode: disarmed"
@app.route('/mode')
def mode():
    global ALARM_MODE
    return ALARM_MODE

@app.route('/setmode', methods=['POST'])
def setmode():
    obj = request.get_json();
    global ALARM_MODE
    ALARM_MODE = obj['mode']
    return "set"


# Sound sensor
def NOISE(PIN):
    print("Sound Detected!")
    global SOUND_DETECTED
    SOUND_DETECTED = "1"

SOUND_PIN = 12
GPIO.setup(SOUND_PIN, GPIO.IN)
GPIO.add_event_detect(SOUND_PIN, GPIO.BOTH, bouncetime=300, callback=NOISE)

def poll_sensor(channel):
        """Poll MCP3002 ADC
        Args:
            channel (int):  ADC channel 0 or 1
        Returns:
            int: 10 bit value relating voltage 0 to 1023
        """
        assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

        # First bit of cbyte is single=1 or diff=0.
        # Second bit is channel 0 or 1
        if channel:
            cbyte = 0b11000000
        else:
            cbyte = 0b10000000

        # Send (Start bit=1, cbyte=sgl/diff & odd/sign & MSBF = 0)
        r = spi.xfer2([1, cbyte, 0])

        # 10 bit value from returned bytes (bits 13-22):
        # XXXXXXXX, XXXX####, ######XX
        return ((r[1] & 31) << 6) + (r[2] >> 2)

@app.route('/water')
def water():
        channel = 0
        channeldata = poll_sensor(channel)

        voltage = round(((channeldata * 3300) / 1024), 0)

        if voltage < 180:
            # Green
            return "NONE"
        elif voltage < 250:
            # Yellow
            return "LOW"
        else:
            # Red
            return "LOTS"

def MOTION(pin):
    print("motion detected")
    global MOTION_DETECTED
    MOTION_DETECTED = "1"
    global ALARM_MODE
    if ALARM_MODE == "Mode: armed":
        camera.save_frame();

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photos')
def photos():
    images = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('photos.html', images=images)

@app.route('/status')
def status():
    try:
        temperature_c = dhtDevice.temperature #get temperature value
        print(temperature_c);
        if temperature_c != None:
            temperature_f = temperature_c * (9 / 5) + 32 #convert to farenhiet
            humidity = dhtDevice.humidity
            return "{:.1f}F  $  {}% ".format(temperature_f, temperature_c, humidity)
    except:
        return "none $ none"


@app.route('/light')
def light():
    if GPIO.input(LIGHT_PIN):
        return("OFF")
    else:
        return("ON")
    
@app.route('/door')
def door():
    if GPIO.input(DOOR_PIN):
        return("OPENED")
    else:
        return("CLOSED")
    
@app.route('/flame')
def flame():
    if GPIO.input(FLAME_PIN):
        return "YES"
    else:
        return "NO"
    
@app.route('/motion')
def motion():
    global MOTION_DETECTED
    return MOTION_DETECTED

@app.route('/sound')
def sound():
    global SOUND_DETECTED
    return SOUND_DETECTED

@app.route('/clear')
def clear():
    global MOTION_DETECTED
    MOTION_DETECTED = "0"
    global SOUND_DETECTED
    SOUND_DETECTED = "0"
    return "cleared"

# Camera
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/video_feed")
def video_feed():
	return Response(gen(camera),
		mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__': 
    app.run( host='0.0.0.0')