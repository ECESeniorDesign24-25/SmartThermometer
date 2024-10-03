from Constants import EMAIL_ADDRESS, OFF_TEMPERATURE #TEMPERATURES # MAX_TEMPERATURE, MIN_TEMPERATURE, OFF_TEMPERATURE
from EmailService import SendEmail
# from GUI.GUI import fahrenheit_to_celsius
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
        current_unit = unit
        print("before 1",current_unit)
        temperatures = PollTemperatureFromESP(sensorNumber=1, unit=current_unit)
        print("after 2", current_unit)

        processed_temp1 = self.proc_temp(temperatures[0], current_unit)
        processed_temp2 = self.proc_temp(temperatures[1], current_unit)

        return processed_temp1, processed_temp2

    def fahrenheit_to_celsius(self, temperature: float):
        return (temperature - 32) * 5 / 9

    def proc_temp(self, temperature, unit):
        if temperature is not None:
            if temperature > self.max_temp and temperature != -110000.0 and temperature != -100000.0:
                self.num_messages += 1
                message = f"Temperature is too high: {round(temperature, 2)} {'F' if unit == 'F' else 'C'}"
                if self.num_messages <= 1:
                    SendEmail(
                        self.email_address,
                        "High Temperature Alert",
                        message,
                    )
                    SendSMS(
                        self.phone_number,
                        self.carrier,
                        message,
                    )
                else:
                    pass
            elif temperature < self.min_temp and temperature != float(
                    OFF_TEMPERATURE) and temperature != -110000.0 and temperature != -100000.0:
                self.num_messages += 1
                message = f"Temperature is too low: {round(temperature, 2)} {'F' if unit == 'F' else 'C'}"
                if self.num_messages <= 1:
                    SendEmail(
                        self.email_address,
                        "Low Temperature Alert",
                        message,
                    )
                    SendSMS(
                        self.phone_number,
                        self.carrier,
                        message,
                    )
                else:
                    pass
            else:
                self.num_messages = 0
        if temperature == float(OFF_TEMPERATURE):
            return None
        if unit == "F" and temperature is not None:
            temperature = self.fahrenheit_to_celsius(temperature)
        return temperature

if __name__ == "__main__":
    # Start()
    pass
