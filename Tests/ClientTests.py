import requests
import time
import sys
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
GUI_DIR = os.path.join(CURR_DIR, "..", "GUI")
sys.path.insert(0, os.path.abspath(GUI_DIR))

from Constants import TEMP1_CHANNEL, TEMP2_CHANNEL, TEMP1_BUTTON_CHANNEL, TEMP2_BUTTON_CHANNEL, ESP32_IP
TEMP_CHANNELS = [TEMP1_CHANNEL, TEMP2_CHANNEL]
TOGGLE_CHANNELS = [TEMP1_BUTTON_CHANNEL, TEMP2_BUTTON_CHANNEL]


def test_channel(host, verbose=False, expected_status=200):
    """
    Checks the response time of a GET request to a channel on the ESP32 server
    """
    if verbose:
        print(f"\n--------------------\nTesting GET request to {host}:")
        curl = os.system(f"curl -vI {host}")
    start = time.time()
    response = requests.get(host)
    end = time.time()
    time_delta = round(end - start, 3)

    assert response.status_code == expected_status
    return time_delta


def test_esp32_server():
    """
    Tests that the average time for 10 requests for each channel is less than 1s
    """
    print("\n--------------------\nTesting ESP32 server:")
    ping = os.system("ping -c 1 " + ESP32_IP)
    if ping != 0:
        print("ESP32 is not connected to the network, skipping.")
        return False

    times = []
    for i in range(10):
        for channel in TEMP_CHANNELS:
            time = test_channel(host=f"{channel}?unit=C")
            times.append(time)
        for channel in TOGGLE_CHANNELS:
            time = test_channel(host=f"{channel}?toggle=ON")
            times.append(time)

    avg_time = sum(times) / len(times)
    print(f"\nAverage time for 10 requests for each channel: {avg_time}s")
    assert avg_time < 1
    return True


def test_esp32_sensor_toggle():
    """
    Tests that the client can toggle the temperature sensors on and off
    """
    print("\n--------------------\nTesting sensor toggle:")
    ping = os.system("ping -c 1 " + ESP32_IP)
    if ping != 0:
        print("ESP32 is not connected to the network, skipping.")
        return

    # verify toggle off works
    toggle1_off = requests.get(url="http://" + ESP32_IP + "/toggle1?toggle=OFF")
    time.sleep(1)
    response1_off = requests.get(url="http://" + ESP32_IP + "/temperature1?unit=C")
    print(toggle1_off.text)

    toggle2_off = requests.get(url="http://" + ESP32_IP + "/toggle2?toggle=OFF")
    print(toggle2_off.text)
    time.sleep(1)
    response2_off = requests.get(url="http://" + ESP32_IP + "/temperature2?unit=C")

    assert response1_off.status_code == 200
    assert response2_off.status_code == 200

    assert response1_off.text == "-100000.00"
    assert response2_off.text == "-100000.00"

    # verify toggle on works
    toggle1_on = requests.get(url="http://" + ESP32_IP + "/toggle1?toggle=ON")
    print(toggle1_on.text)
    time.sleep(1)
    response1_on = requests.get(url="http://" + ESP32_IP + "/temperature1?unit=C")

    toggle2_on = requests.get(url="http://" + ESP32_IP + "/toggle2?toggle=ON")
    print(toggle2_on.text)
    time.sleep(1)
    response2_on = requests.get(url="http://" + ESP32_IP + "/temperature2?unit=C")

    assert response1_on.status_code == 200
    assert response2_on.status_code == 200

    assert response1_on.text != "-100000.00"
    assert response2_on.text != "-100000.00"


def test_invalid_channel_request():
    """
    Test that the server returns a 400 status code when an invalid parameter is passed
    """
    print("\n--------------------\nTesting invalid channel request:")
    for channel in TEMP_CHANNELS:
        test_channel(
            host=f"{channel}?invalidParam=C",
            expected_status=400,
        )
    for channel in TOGGLE_CHANNELS:
        test_channel(
            host=f"{channel}?invalidParam=ON",
            expected_status=400,
        )
        test_channel(
            host=f"{channel}",
            expected_status=200,
        )


if __name__ == "__main__":
    server_up = test_esp32_server()
    if server_up:
        test_esp32_sensor_toggle()
        test_invalid_channel_request()
