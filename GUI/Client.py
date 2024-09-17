from Constants import EMAIL_ADDRESS
from EmailService import SendEmail
from SMSService import SendSMS

def Start():
    print("Starting the client")
    email_success = SendEmail(EMAIL_ADDRESS, "Test", "Test")
    if email_success:
        print("Email sent successfully")

    sms_success = SendSMS("6087974248", "VERIZON", "Test")
    if sms_success:
        print("SMS sent successfully")

if __name__ == "__main__":
    Start()