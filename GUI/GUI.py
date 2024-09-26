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

@app.route('/')
def home():
    return render_template("gui.html")

@app.route('/temperature1', methods=['GET'])
def handle_temperature_from_sensor1():
    temp = PollTemperatureFromESP(sensorNumber=1, unit="C")
    main_client.ProcessTemperature(1, 'C')
    print("sensor 1", temp)
    return jsonify(temperature=temp)

@app.route('/temperature2', methods=['GET'])
def handle_temperature_from_sensor2():
    temp = PollTemperatureFromESP(sensorNumber=2, unit="C")
    main_client.ProcessTemperature(2, 'C')
    # return response.text
    print("sensor 2", temp)
    return jsonify(temperature=temp)


@app.route('/power_off', methods=['GET'])
def handle_power_off():
    try:
        requests.post(f"{ESP32_SERVER}/toggle1?toggle=OFF")
        requests.post(f"{ESP32_SERVER}/toggle2?toggle=OFF")
    except requests.exceptions.ConnectionError:
        return {"status": "Failed"}, 500

    return {"status": "Success"}, 201

@app.route('/power_on', methods=['GET'])
def handle_power_on():
    try:
        requests.post(f"{ESP32_SERVER}/toggle1?toggle=ON")
        requests.post(f"{ESP32_SERVER}/toggle2?toggle=ON")
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
    os.environ["MIN_TEMP"] = str(min_temp)
    os.environ["MAX_TEMP"] = str(max_temp)
    main_client.set_max_temp(float(max_temp))
    main_client.set_min_temp(float(min_temp))
    print(min_temp, max_temp)
    return {"status": "Success"}, 201


# @app.route('switch_scale', methods=['POST'])
# def handle_switch_scale():
#     pass


if __name__ == '__main__':
    app.run()

