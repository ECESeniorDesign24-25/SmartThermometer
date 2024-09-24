import requests
from Constants import (
    TEMP1_CHANNEL,
    TEMP2_CHANNEL,
    TEMP1_BUTTON_CHANNEL,
    TEMP2_BUTTON_CHANNEL,
)


def PollTemperatureFromESP(sensorNumber: int):
    """
    Polls the current temperature from the ESP32 web server
    """
    try:
        if sensorNumber == 1:
            url = TEMP1_CHANNEL
        elif sensorNumber == 2:
            url = TEMP2_CHANNEL
        else:
            return None
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        temperature = float(response.text.split()[0])
        return temperature
    except requests.exceptions.RequestException as e:
        return None


def ToggleSensorOnESP(sensorNumber: int, toggle: int):
    """
    Sends message to the ESP web server to toggle a given sensor (temperature sensor 1 or 2)
    on/off
    """
    try:
        if sensorNumber == 1:
            url = TEMP1_BUTTON_CHANNEL
        elif sensorNumber == 2:
            url = TEMP2_BUTTON_CHANNEL
        else:
            return False
        message = requests.post(url, data=toggle, timeout=5)
        if message.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
