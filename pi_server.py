from flask import Flask, jsonify, request
import board
import adafruit_tcs34725
import RPi.GPIO as GPIO

app = Flask(__name__)

# setup the output pin for controlling the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

# setup communication with the sensor using i2c
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

# end-point for getting the current status of the IOT device
@app.route('/', methods = ['GET', 'POST'])
def get_status():
    # this is used to determine if the light is currenty on or off
    light = GPIO.input(23)
    # this gets the current colour and light information from the sensor
    lux = sensor.lux
    temp = sensor.color_temperature
    color_rgb = sensor.color_rgb_bytes
    # all the information gets packed into JSON and sent to the client
    return jsonify({'light': light, 'lux': lux, 'temp': temp, 'color_rgb': color_rgb})

# end-point for turning on the light
@app.route('/light_on/', methods = ['GET', 'POST'])
def light_on():
    # turns the appropriate pin on
    GPIO.output(23, True)
    # send the status of the pin back to the client for confirmation
    light = GPIO.input(23)
    return jsonify({'light': light})

# end-point for turning off the light
@app.route('/light_off/', methods = ['GET', 'POST'])
def light_off():
    GPIO.output(23, False)
    light = GPIO.input(23)
    return jsonify({'light': light})

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 80)
