import requests
import time 
import os

def test_channel(ip, channel, function, initial=False): 
    """ 
    Checks the response time of a GET or POST request to a channel on the ESP32 server
    """
    host = f"{ip}{channel}?unit=C"
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

    if initial:
        print(f"Channel: {channel} | Response Code: {response} | Time: {time_delta}s" )
    assert response.status_code == 200
    assert time_delta < 1
    return time_delta

def test_esp32_server():
    """
    Tests that the average time for 10 requests for each channel is less than 1s
    """
    esp32_ip = "192.168.1.25"
    get_channels = ["/temperature1", "/temperature2"]
    post_channels = ["/toggle1", "/toggle2"]

    ping = os.system("ping -c 1 " + esp32_ip)
    if ping != 0:
        print("ESP32 is not connected to the network, skipping.")
        return

    times = []
    for i in range(10):
        for channel in get_channels:
            time = test_channel(esp32_ip, channel, "GET")
            times.append(time)
        for channel in post_channels:
            time = test_channel(esp32_ip, channel, "POST")
            times.append(time)

    avg_time = sum(times) / len(times)
    print(f"\nAverage time for 10 requests for each channel: {avg_time}s")
    assert avg_time < 1

if __name__ == "__main__":
    test_esp32_server()