import os
from IPListener import getIP

# User constants
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
CARRIERS = {
    "ATT": "@mms.att.net",
    "TMOBILE": " @tmomail.net",
    "VERIZON": "@vtext.com",
    "SPRINT": "@page.nextel.com",
}

# Temperature constants
MAX_TEMPERATURE = 100.0
MIN_TEMPERATURE = 0.0
OFF_TEMPERATURE = -100000.00


# ESP32 web server channels
ESP32_IP = getIP()
ESP32_SERVER = "http://" + ESP32_IP
TEMP1_CHANNEL = ESP32_SERVER + "/temperature1"
TEMP2_CHANNEL = ESP32_SERVER + "/temperature2"
TEMP1_BUTTON_CHANNEL = ESP32_SERVER + "/toggle1"
TEMP2_BUTTON_CHANNEL = ESP32_SERVER + "/toggle2"
