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
OFF_TEMPERATURE = -100000.00
ESP32_SERVER = "http://192.168.1.25"

TEMP1_CHANNEL = ESP32_SERVER + "/temperature1"
TEMP2_CHANNEL = ESP32_SERVER + "/temperature2"
TEMP1_BUTTON_CHANNEL = ESP32_SERVER + "/toggle1"
TEMP2_BUTTON_CHANNEL = ESP32_SERVER + "/toggle2"

