from Constants import EMAIL_ADDRESS, MAX_TEMPERATURE, MIN_TEMPERATURE
from EmailService import SendEmail
from SMSService import SendSMS
from Receiver import Receiver
from ESPUtils import PollTemperatureFromESP


def Start():
    """
    Main loop
    """
    receiver = Receiver(EMAIL_ADDRESS, "6087974248", "VERIZON")

    while True:
        temperature1 = ProcessTemperature(receiver=receiver, sensor=1, unit="C")
        temperature2 = ProcessTemperature(receiver=receiver, sensor=2, unit="C")

def ProcessTemperature(receiver: Receiver, sensor: int=1, unit: str="C"):
    """
    Polls the temperature from the ESP32, and sends an email and SMS if the temperature exceeds MAX_TEMPERATURE
    """
    temperature = PollTemperatureFromESP(sensorNumber=sensor, unit=unit)
    if temperature is not None:
        if temperature > MAX_TEMPERATURE:
            SendEmail(
                receiver.emailAddress,
                "High Temperature Alert",
                f"Temperature is too high: {temperature}",
            )
            SendSMS(
                receiver.phoneNumber,
                receiver.cellCarrier,
                f"Temperature is too high: {temperature}",
            )
        elif temperature < MIN_TEMPERATURE and temperature != OFF_TEMPERATURE:
            SendEmail(
                receiver.emailAddress,
                "Low Temperature Alert",
                f"Temperature is too low: {temperature}",
            )
            SendSMS(
                receiver.phoneNumber,
                receiver.cellCarrier,
                f"Temperature is too low: {temperature}",
            )
    if temperature == OFF_TEMPERATURE:
        temperature = None
    return temperature


if __name__ == "__main__":
    Start()
