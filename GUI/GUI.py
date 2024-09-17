import requests
from flask import Flask, render_template, request, jsonify, redirect
from Constants import ESP32_SERVER
from Client import Start
from ESPUtils import PollTemperatureFromESP, ToggleSensorOnESP
from Constants import TEMPERATURES
import os

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("gui.html")

@app.route('/temperature1', methods=['GET'])
def handle_temperature_from_sensor1():
    temp = PollTemperatureFromESP(sensorNumber=1, unit="C")

    print("sensor 1", temp)
    return jsonify(temperature=temp)

@app.route('/temperature2', methods=['GET'])
def handle_temperature_from_sensor2():
    temp = PollTemperatureFromESP(sensorNumber=2, unit="C")

    # return response.text
    print("sensor 2", temp)
    return jsonify(temperature=temp)


@app.route('/power_off', methods=['POST'])
def handle_power_off():
    try:
        requests.post(f"{ESP32_SERVER}/toggle1?toggle=OFF")
        requests.post(f"{ESP32_SERVER}/toggle2?toggle=OFF")
    except requests.exceptions.ConnectionError:
        pass


@app.route('/power_on', methods=['POST'])
def handle_power_on():
    try:
        requests.post(f"{ESP32_SERVER}/toggle1?toggle=ON")
        requests.post(f"{ESP32_SERVER}/toggle2?toggle=ON")
    except requests.exceptions.ConnectionError:
        pass

@app.route('/user', methods=['POST'])
def handle_user_info():
   carrier = request.form.get('carrier')
   phone = request.form.get('phone')
   email = request.form.get('email')
   print(carrier, phone, email)
   Start(carrier, phone, email)

   return {"status": "success"}, 200


@app.route('/max_min', methods=['POST'])
def handle_min_max():
    min = request.form.get('min')
    max = request.form.get('max')
    os.environ["MIN_TEMP"] = str(min)
    os.environ["MAX_TEMP"] = str(max)
    # TEMPERATURES["MIN_TEMP"] = request.form.get('min_temp')
    # TEMPERATURES["MAX_TEMP"] = request.form.get('max_temp')
    print(min, max)
    return {"status": "success"}, 200


# @app.route('switch_scale', methods=['POST'])
# def handle_switch_scale():
#     pass


if __name__ == '__main__':
    app.run()

