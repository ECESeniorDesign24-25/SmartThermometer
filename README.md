# SmartThermometer

### Arduino IDE Setup:
1. Install [ESPAsyncWebServer library](https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip), extract + rename the download to ESPAsyncWebServer, and move the folder to your Arduino/libraries directory
2. Install [AsyncTCP library](https://github.com/me-no-dev/AsyncTCP/archive/refs/heads/master.zip), extract + rename the download to AsyncTCP, and move the folder to your Arduino/libraries directory
3. Make sure the following libraries are downloaded into the libraries/ folder inside your sketch folder:
    - ESPAsyncWebServer
    - AsyncTCP
    - DallasTemperature
    - LiquidCrystal


> You might need to restart your Arduino IDE for the updates to take place

#### Update the WiFiCredentials.h file with your personal username and password. Once this is updated, run the following in your terminal:
    - git update-index --assume-unchanged ESP32/WiFiCredentials.h
      
> This will prevent git from adding the updated file with your personal credentials to the remote repository.

### Client Services Setup:
1. This application uses the Gmail SMTP server which requires an app-specific password. To set this password, add an app-specific password at [this link](https://myaccount.google.com/apppasswords).
2. Once this password is set, update the set_creds.sh script with the following:
   
#### For Unix systems:
    - export EMAIL_ADDRESS="[Your email address]"
    - export EMAIL_PASSWORD="[Your app-specific password]"
Then run the following in your terminal:
```
chmod +x set_creds.sh
source ./set_creds.sh
```


#### For Windows systems:
1. Change the name from set_creds.sh to set_creds.bat
2. Change the "export" to "set" like so:
```
set EMAIL_ADDRESS="[Your email address]"
set EMAIL_PASSWORD="[Your app-specific password]"
```
Then run the following in your terminal:
```
set_creds.bat
```

You must also run the following:
```
git update-index --assume-unchanged set_creds.sh
```


### Testing:
The Tests/ directory handles the automated testing suite for various functions across the source code. 

To test ESP functions, add a test to the ESPTests.cpp file. Note: if you test a function that depends on an Arduino library, you must add a Mock library to the lib/ directory (See ArduinoMock.cpp).

To test Client functions, add a test to the ClientTests.py file. Note: any test that depends on reading from the ESP32 server should skip if the ESP32 is not connected.

All tests are run through run_tests.sh, which gets called in a GitHub Actions script on each new PR.

### How to talk to the server:
You can make HTTP requests to http://192.168.1.25 (faster) or http://esp32.local (slower). The available channels are:
1. /temperature1 (returns temperature from temperature sensor #1 on GET, supports parameter "unit" [C or F])
2. /temperature2 (returns temperature from temperature sensor #2 on GET, supports parameter "unit" [C or F])
3. /toggle1 (sets temperature sensor #1 status on GET, supports parameter "toggle" [ON or OFF])
4. /toggle2 (sets temperature sensor #2 status on GET, supports parameter "toggle" [ON or OFF])

>Example:
> curl -X GET http://192.168.1.25/temperature1?unit=C
> curl -X GET http://192.168.1.25/toggle1?toggle=ON