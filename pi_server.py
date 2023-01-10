from flask import Flask, jsonify, request
import board
import adafruit_tcs34725
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

@app.route('/', methods = ['GET', 'POST'])
def get_status():

    if (request.method == 'GET'):
        light = GPIO.input(23)
        color = sensor.color
        lux = sensor.lux
        temp = sensor.color_temperature
        color_rgb = sensor.color_rgb_bytes
        return jsonify({'light': light, 'lux': lux, 'temp': temp, 'color_rgb': color_rgb})

@app.route('/light_on/', methods = ['GET', 'POST'])
def light_on():
    GPIO.output(23, True)
    light = GPIO.input(23)
    return jsonify({'light': light})

@app.route('/light_off/', methods = ['GET', 'POST'])
def light_off():
    GPIO.output(23, False)
    light = GPIO.input(23)
    return jsonify({'light': light})

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
