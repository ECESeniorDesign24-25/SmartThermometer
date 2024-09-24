import requests
import time 
import os

def test_channel(ip, channel, function):
    url = f"http://{ip}{channel}"

    print(f"\n--------------------\nTesting {function} request to {url}:")
    curl = os.system(f"curl -vI {url}")
    start = time.time()
    if function == "GET":
        response = requests.get(channel)
    elif function == "POST":
        response = requests.post(channel)
    end = time.time()
    time_delta = round(end - start, 3)
    print(f"Channel: {channel} | Response Code: {response} | Time: {time_delta}s" )
    assert response.status_code == 200
    assert time_delta < 1

def test_esp32_server():
    esp32_ip = "192.168.1.25"
    get_channels = ["/temperature1", "/temperature2"]
    post_channels = ["/toggle1", "/toggle2"]

    ping = os.system("ping -c 1 " + esp32_ip)
    if ping != 0:
        print("ESP32 is not connected to the network, skipping.")
        return

    for channel in get_channels:
        test_channel(esp32_ip, channel, "GET")
    for channel in post_channels:
        test_channel(esp32_ip, channel, "POST")

if __name__ == "__main__":
    test_esp32_server()