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
    emailResult = SendEmail(
        receiver, "Temperature Monitor Started", "Temperature monitor has started"
    )
    smsResult = SendSMS(receiver, "Temperature monitor has started")

    if emailResult:
        print("Email sent")
    else:
        print("Email failed to send")

    if smsResult:
        print("SMS sent")
    else:
        print("SMS failed to send")


def ProcessTemperature(receiver: Receiver, message: str):
    """
    Polls the temperature from the ESP32, and sends an email and SMS if the temperature exceeds MAX_TEMPERATURE
    """
    temperature = PollTemperatureFromESP()
    if temperature is not None:
        if temperature > MAX_TEMPERATURE:
            SendEmail(receiver.emailAddress, "High Temperature Alert", message)
            SendSMS(receiver.phoneNumber, receiver.cellCarrier, message)
        elif temperature < MIN_TEMPERATURE:
            SendEmail(receiver.emailAddress, "Low Temperature Alert", message)
            SendSMS(receiver.phoneNumber, receiver.cellCarrier, message)
    else:
        print("Error polling temperature")


if __name__ == "__main__":
    Start()
