from flask import Flask, render_template, redirect, request
import requests
import sys
import time
from threading import Thread, Lock

pi_address = sys.argv[1]
app = Flask(__name__)

historical_lux = []

class TaskClass:
    def __init__(self):
        self.setting = 2
        self.min_brightness_level = 60
        self._lock = Lock()
    def update_light(self, setting, brightness):
        with self._lock:
            self.setting = setting
            #self.min_brightness_level = brightness
    def task(self):
        while True:
            data = requests.get("http://{}".format(pi_address)).json()
            lux = float(data["lux"])
            if len(historical_lux) < 30:
                historical_lux.append(lux)
            else:
                historical_lux.pop(0)
                historical_lux.append(lux)
            
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