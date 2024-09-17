import requests
from Constants import ESP32_IP

def PollTemperatureFromESP():
    """
    Polls the current temperature from the ESP32 web server
    """
    while True:
        try:
            response = requests.get(ESP32_IP, data={'temperature': '1'})
            if response.status_code == 200:
                return response.text
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

def ToggleSensorOnESP(sensorNumber: int, toggle: int):
    """
    Sends message to the ESP web server to toggle a given sensor (temperature sensor 1 or 2) 
    on/off
    """
    try:
        message = requests.post(ESP32_IP, data={'sensor': sensorNumber, 'toggle': toggle})
        if message.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def GetSensorStatusFromESP(sensorNumber: int):
    """
    Polls the ESP web server for the status of a given sensor
    """
    try:
        response = requests.get(ESP32_IP, data={'sensor': sensorNumber})
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def GetESPStatus():
    """ 
    Polls the ESP for the status of the on/off power switch
    """
    try:
        response = requests.get(ESP32_IP, data={'status': '1'})
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
