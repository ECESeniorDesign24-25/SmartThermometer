# SmartThermometer Setup Docs

### Repository Setup:

Step 1 to set up the project is to clone this repository by running the following in your terminal:
```
git clone https://github.com/ECESeniorDesign24-25/SmartThermometer.git
```

### Programming Setup (Arduino IDE):
1. IDE Setup:
    - Use the Arduino IDE with the esp32 board provided by Espressif Systems. <strong>Important: You MUST use Version 2.0.17</strong>, not the latest. This will allow connection to enterprise WiFi networks (such as eduroam).
    - Select ESP32 Dev Module with the USB port that you connected to the ESP32 with.
2. Libary Setup
    - Install [ESPAsyncWebServer library](https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip), extract + rename the download to ESPAsyncWebServer, and move the folder to wherever the rest of your Arduino Core libraries are stored.
    - In Library Manager on the Arduino IDE, install the following libraries with their specified versions:
        * AsyncTCP [1.1.4]
        * LiquidCrystal [1.0.7]
        * OneWire [2.3.8]
        * DallasTemperature [3.9.0]
3. Update the [ESP32/Constants.h](ESP32/Constants.h) file with the WiFi credentials of the network you want to connect to.
   ```
   // the name of your network
   #define WIFI_SSID ""

   // the username for enterprise networks (Don't change this for personal networks!)
   #define WIFI_USERNAME ""

   // the WiFi password
   #define WIFI_PASSWORD ""
   ```
4. Compile & upload your code to the ESP32. Note: You may need to reset the ESP32 (clicking the "EN" button) and power cycle after upload for the new code to load.
5. You should see serial output on your computer with a 115200 baud rate.


### GUI Setup (Python Client) TODO

### Troubleshooting
1. You can run the Tests/run_client_tests.sh file to quickly verify connection between PC and ESP32. Note: You must be on the same WiFi network as the ESP32:
    MacOS/Unix: `./Tests/run_client_tests.sh`
   
3. If the test outputs "Skipping tests", then there was an issue with the test script connecting to the ESP32. You can manuallly try to connect through your command line. In your serial console when running the ESP32 code, you should see:
   ```
   Connected to <WiFi Address> with IP Address: <IP Address>
   ```
    If you don't see this, try resetting your ESP32. It should show up again after that.
    Then, in your terminal (MacOS/Unix), you can run the following to see if connection is possible:
   ```
   ping <IP Address>
   ```
   If connection was successful, you should see something like this in your terminal output:
   ```
   PING <IP Address> (<IP Address>): 56 data bytes
   64 bytes from <IP Address>: icmp_seq=0 ttl=63 time=6.954 ms
   ```
   
4. Once you are able to ping the ESP32, you can now manually make HTTP requests to the ESP32 Web Server. Here are the supported requests:
   - Request temperature from a sensor:
       ```
       curl <IP Address>/temperature1?unit=C
       ```
       This will return the temperature from temperature sensor 1 in celsius. You can make the same request to sensor 2 by changing temperature1 to temperature2, and you can change the unit to fahrenheit by changing unit=C to unit=F.
   - Toggle a sensor on or off:
     ```
     curl <IP Address>/toggle1?toggle=OFF
     ```
     This will turn temperature sensor 1 off. You can make the same request to sensor 2 by changing temperature1 to temperature2, and you can turn the sensor back on by changing toggle=ON.

