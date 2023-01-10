from flask import Flask, render_template, redirect, request
import requests
import sys
import time
from threading import Thread, Lock

# address of the pi should be passed as an argument to this program
pi_address = sys.argv[1]
app = Flask(__name__)

# data about brigtness from the last 30 seconds
historical_lux = []

# a class that deals with turning on and off the light as well as recording brightness levels
class TaskClass:
    def __init__(self):
        # the light is set to turn on and off automatically by default at a minimum brightness level of 60 Lux
        self.setting = 2
        self.min_brightness_level = 60
        self._lock = Lock()
    def update_light(self, setting, brightness):
        with self._lock:
            self.setting = setting
            self.min_brightness_level = brightness
    # the function which does the job of controlling the light and fetching the brightness data
    def task(self):
        while True:
            # gets the current status of the pi based lighting control and monitoring device
            data = requests.get("http://{}".format(pi_address)).json()
            # seperates out the data concerning brightness and updates the record of brightness
            lux = float(data["lux"])
            if len(historical_lux) < 30:
                historical_lux.append(lux)
            else:
                historical_lux.pop(0)
                historical_lux.append(lux)
            
            # deals with turning the light on or off according to the setting
            if self.setting == 0:
                requests.get("http://{}/light_off".format(pi_address))
            elif self.setting == 1:
                requests.get("http://{}/light_on".format(pi_address))
            else:
                if lux < self.min_brightness_level:
                    requests.get("http://{}/light_on".format(pi_address))
                else:
                    requests.get("http://{}/light_off".format(pi_address))

            time.sleep(1)

@app.route("/")
def home():
    data = requests.get("http://{}".format(pi_address)).json()
    return render_template("index.html", data=data)

# renders the graph using the historial data collected by the TaskClass.task function
@app.route("/graph")
def graph():
    return render_template("graph.html", data=historical_lux, length=len(historical_lux))

@app.route("/light_setting", methods=["POST"])
def light_setting():
    form = request.form
    setting = form["light_setting"]
    print(setting)
    if setting == "on":
        taskItem.update_light(1, 60)
    if setting == "off":
        taskItem.update_light(0, 60)
    if setting == "auto":
        taskItem.update_light(2, 60)
    return redirect("/")

if __name__ == "__main__":
    taskItem = TaskClass()
    thread1 = Thread(target=taskItem.task)
    thread1.start()
    app.run(host='0.0.0.0', port=8080)
