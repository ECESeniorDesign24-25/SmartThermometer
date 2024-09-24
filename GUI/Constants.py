import os

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
CARRIERS = {
    "ATT": "@mms.att.net",
    "TMOBILE": " @tmomail.net",
    "VERIZON": "@vtext.com",
    "SPRINT": "@page.nextel.com",
}
MAX_TEMPERATURE = 100.0
MIN_TEMPERATURE = 0.0
ESP32_SERVER = "http://esp32.local/"

TEMP1_CHANNEL = ESP32_SERVER + "/temp1"
TEMP2_CHANNEL = ESP32_SERVER + "/temp2"
TEMP1_BUTTON_CHANNEL = ESP32_SERVER + "/toggle1"
TEMP2_BUTTON_CHANNEL = ESP32_SERVER + "/toggle2"
