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
        temperature = ProcessTemperature(receiver)


def ProcessTemperature(receiver: Receiver):
    """
    Polls the temperature from the ESP32, and sends an email and SMS if the temperature exceeds MAX_TEMPERATURE
    """
    temperature = PollTemperatureFromESP()
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
        elif temperature < MIN_TEMPERATURE:
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
    return temperature


if __name__ == "__main__":
    Start()
