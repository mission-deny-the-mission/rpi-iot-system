import requests
import time
import sys

pi_address = sys.argv[1]
if len(sys.argv) > 2:
    min_brightness_level = float(sys.argv[2])
else:
    min_brightness_level = 60

while True:
    response = requests.get("http://{}".format(pi_address))
    data = response.json()
    if data["light"]:
        print("Light status: on")
    else:
        print("Light status: off")
    print("Brightness: {} lux".format(data["lux"]))
    print("Color Temperature: {}".format(data["temp"]))

    if data["lux"] < min_brightness_level:
        requests.get("http://{}/light_on/".format(pi_address))
        print("turned light on")
    else:
        requests.get("http://{}/light_off/".format(pi_address))
        print("turned light off")

    time.sleep(1)