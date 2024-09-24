import requests
import time
import os

ESP32_IP = "192.168.1.25"
TEMP_CHANNELS = ["/temperature1", "/temperature2"]
TOGGLE_CHANNELS = ["/toggle1", "/toggle2"]


def test_channel(function, host, initial=False, expected_status=200):
    """
    Checks the response time of a GET or POST request to a channel on the ESP32 server
    """
    url = "http://" + host
    if initial:
        print(f"\n--------------------\nTesting {function} request to {host}:")
        curl = os.system(f"curl -vI {url}")
    start = time.time()
    if function == "GET":
        response = requests.get(url)
    elif function == "POST":
        response = requests.post(url)
    end = time.time()
    time_delta = round(end - start, 3)

    assert response.status_code == expected_status
    assert time_delta < 1
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
            time = test_channel(host=f"{ESP32_IP}{channel}?unit=C", function="GET")
            times.append(time)
        for channel in TOGGLE_CHANNELS:
            time = test_channel(host=f"{ESP32_IP}{channel}?toggle=ON", function="GET")
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
    requests.get(url="http://" + ESP32_IP + "/toggle1?toggle=OFF")
    time.sleep(1)
    response1 = requests.get(url="http://" + ESP32_IP + "/temperature1?unit=C")

    requests.get(url="http://" + ESP32_IP + "/toggle2?toggle=OFF")
    time.sleep(1)
    response2 = requests.get(url="http://" + ESP32_IP + "/temperature2?unit=C")

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response1.text == "-100000.00"
    assert response2.text == "-100000.00"

    # verify toggle on works
    requests.get(url="http://" + ESP32_IP + "/toggle1?toggle=ON")
    time.sleep(1)
    response1 = requests.get(url="http://" + ESP32_IP + "/temperature1?unit=C")

    requests.get(url="http://" + ESP32_IP + "/toggle2?toggle=ON")
    time.sleep(1)
    repsonse2 = requests.get(url="http://" + ESP32_IP + "/temperature2?unit=C")

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response1.text != "-100000.00"
    assert response2.text != "-100000.00"


def test_invalid_channel_request():
    """
    Test that the server returns a 400 status code when an invalid parameter is passed
    """
    print("\n--------------------\nTesting invalid channel request:")
    for channel in TEMP_CHANNELS:
        test_channel(
            host=f"{ESP32_IP}{channel}?invalidParam=C",
            function="GET",
            expected_status=400,
        )
    for channel in TOGGLE_CHANNELS:
        test_channel(
            host=f"{ESP32_IP}{channel}?invalidParam=ON",
            function="GET",
            expected_status=400,
        )


if __name__ == "__main__":
    server_up = test_esp32_server()
    if server_up:
        test_esp32_sensor_toggle()
