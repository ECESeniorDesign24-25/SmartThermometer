from Constants import EMAIL_ADDRESS, OFF_TEMPERATURE #TEMPERATURES # MAX_TEMPERATURE, MIN_TEMPERATURE, OFF_TEMPERATURE
from EmailService import SendEmail
from SMSService import SendSMS
from Receiver import Receiver
from ESPUtils import PollTemperatureFromESP


class ReceivingClient:
    def __init__(self, email_address: str = EMAIL_ADDRESS, phone_number: str =  "6087974248" , carrier: str = "VERIZON"):
        self.email_address = email_address
        self.phone_number = phone_number
        self.carrier = carrier
        self.max_temp = 30
        self.min_temp = 19
        self.num_messages = 0

    def set_email_address(self, email_address: str):
        self.email_address = email_address

    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number

    def set_carrier(self, carrier: str):
        self.carrier = carrier

    def set_max_temp(self, max_temp: float):
        self.max_temp = max_temp

    def set_min_temp(self, min_temp: float):
        self.min_temp = min_temp

    def get_phone_number(self):
        return self.phone_number

    def get_carrier(self):
        return self.carrier

    def get_email_address(self):
        return self.email_address

    def reset_num_messages(self):
        self.num_messages = 0

    def ProcessTemperature(self, sensor: int = 1, unit: str = "C"):
        """
        Polls the temperature from the ESP32, and sends an email and SMS if the temperature exceeds MAX_TEMPERATURE
        """
        temperature = PollTemperatureFromESP(sensorNumber=sensor, unit=unit)
        if temperature is not None:
            if temperature > self.max_temp and temperature != -110000.0 and temperature != -100000.0:
                self.num_messages += 1
                if self.num_messages <= 1:
                    SendEmail(
                        self.email_address,
                        "High Temperature Alert",
                        f"Temperature is too high: {temperature}",
                    )
                    SendSMS(
                        self.phone_number,
                        self.carrier,
                        f"Temperature is too high: {temperature}",
                    )
                else:
                    pass
            elif temperature < self.min_temp and temperature != float(
                    OFF_TEMPERATURE) and temperature != -110000.0 and temperature != -100000.0:
                self.num_messages += 1
                if self.num_messages <= 1:
                    SendEmail(
                        self.email_address,
                        "Low Temperature Alert",
                        f"Temperature is too low: {temperature}",
                    )
                    SendSMS(
                        self.phone_number,
                        self.carrier,
                        f"Temperature is too low: {temperature}",
                    )
                else:
                    pass
            else:
                self.num_messages = 0
        if temperature == float(OFF_TEMPERATURE):
            temperature = None
        return temperature


if __name__ == "__main__":
    # Start()
    pass
