import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from Constants import ESP32_SERVER
# from Client import Start
from ESPUtils import PollTemperatureFromESP, ToggleSensorOnESP
from Constants import TEMPERATURES
import os
from Client import ReceivingClient

app = Flask(__name__)


main_client = ReceivingClient()

# global unit
unit = 'C'
status1 = 1
status2 = 1

@app.route('/')
def home():
    return render_template("gui.html")

@app.route('/temperature', methods=['GET'])
def handle_temperature_from_sensor1():
    temp1, temp2 = main_client.ProcessTemperature(1, unit)
    # temp2 = main_client.ProcessTemperature(2, unit)
    if app.config['TESTING']:
        temp1 = 20
        temp2 = 30
    print("sensor 1", temp1)
    print("sensor 2", temp2)
    return jsonify(temperature1=temp1, temperature2=temp2, tempscale=unit)


@app.route('/toggle1', methods=['GET'])
def handle_power_off():
    global status1
    if status1 == 0:
        status1 = 1
        try:
            print("turning on")
            requests.get(f"{ESP32_SERVER}/toggle1?toggle=ON")
        except requests.exceptions.ConnectionError:
            return {"status": "failed"}, 500
    else:
        status1 = 0
        try:
            print("turning off")
            requests.get(f"{ESP32_SERVER}/toggle1?toggle=OFF")
        except requests.exceptions.ConnectionError:
            return {"status": "Failed"}, 500

    return {"status": "Success"}, 201

@app.route('/toggle2', methods=['GET'])
def handle_power_on():
    global status2
    if status2 == 0:
        status2 = 1
        try:
            print("turning On")
            requests.get(f"{ESP32_SERVER}/toggle2?toggle=ON")
        except requests.exceptions.ConnectionError:
            return {"status": "Failed"}, 500
    else:
        status2 = 0
        try:
            print("turning Off")
            requests.get(f"{ESP32_SERVER}/toggle2?toggle=OFF")
        except requests.exceptions.ConnectionError:
            return {"status": "Failed"}, 500

    return {"status": "Success"}, 201

@app.route('/user', methods=['GET'])
def handle_user_info():
    carrier = request.args.get('carrier')
    phone = request.args.get('phone')
    email = request.args.get('email')
    main_client.set_carrier(carrier)
    main_client.set_phone_number(phone)
    main_client.set_email_address(email)
    print(carrier, phone, email)
    # Start(carrier, phone, email)

    return {"status": "Success"}, 201

@app.route('/max_min', methods=['GET'])
def handle_min_max():
    min_temp = request.args.get('min')
    max_temp = request.args.get('max')
    # os.environ["MIN_TEMP"] = str(min_temp)
    # os.environ["MAX_TEMP"] = str(max_temp)
    main_client.set_max_temp(float(max_temp))
    main_client.set_min_temp(float(min_temp))
    main_client.reset_num_messages()
    print(min_temp, max_temp)
    return {"status": "Success"}, 201


@app.route('/switch_scale', methods=['GET'])
def handle_switch_scale():
    global unit
    if unit == "C":
        unit = "F"
    else:
        unit = "C"
    return {"status": "Success", "unit": unit}, 201

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

if __name__ == '__main__':
    app.run(threaded=True)

