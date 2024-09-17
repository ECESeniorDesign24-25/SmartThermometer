# SmartThermometer

[wip] Setup (Arduino IDE):
1. Install [ESPAsyncWebServer library](https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip), extract + rename the download to ESPAsyncWebServer, and move the folder to your Arduino/libraries directory
2. Install [AsyncTCP library](https://github.com/me-no-dev/AsyncTCP/archive/refs/heads/master.zip), extract + rename the download to AsyncTCP, and move the folder to your Arduino/libraries directory

> You might need to restart your Arduino IDE for the updates to take place

3. Update the WiFiCredentials.h file with your personal username and password. This file doesn't get added to GitHub, so any changes you make won't appear in the repository.

Email Setup:
1. This application uses the Gmail SMTP server which requires an app-specific password. To set this password, add an app-specific password at [this link](https://myaccount.google.com/apppasswords).
2. Once this password is set, run the following in your terminal:
- On Mac/Linux:
    - export EMAIL_ADDRESS="[YOUR_EMAIL_HERE]"
    - export EMAIL_PASSWORD="[YOUR_APP_SPECIFIC_PASSWORD_HERE]"
- On Windows:
    - set EMAIL_ADDRESS="[YOUR_EMAIL_HERE]"
    - set EMAIL_PASSWORD="[YOUR_APP_SPECIFIC_PASSWORD_HERE]"
