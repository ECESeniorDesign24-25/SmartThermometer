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

