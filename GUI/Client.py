from EmailService import SendEmail
from Constants import EMAIL_ADDRESS

def Start():
    print("Starting the client")
    success = SendEmail(EMAIL_ADDRESS, "Test", "Test")
    if success:
        print("Email sent successfully")

if __name__ == "__main__":
    Start()