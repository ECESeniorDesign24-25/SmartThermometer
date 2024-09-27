import smtplib
from Receiver import Receiver
from Constants import EMAIL_ADDRESS, EMAIL_PASSWORD, CARRIERS


def SendSMS(client_phone, client_carrier, message: str):
    """
    Sends an SMS to the given receiver phone number
    """
    try:
        receiverNumber = f"{client_phone}{CARRIERS[client_carrier]}"
        if not EMAIL_ADDRESS or EMAIL_ADDRESS == "":
            print(
                "Invalid 'from' email address. Set it by running: \n\texport EMAIL_ADDRESS='[your email address]'"
            )
            raise Exception("Invalid 'from' email address")
        if not EMAIL_ADDRESS or EMAIL_ADDRESS == "":
            print(
                "Invalid 'from' email password. Set it by running: \n\texport EMAIL_PASSWORD='[your email password]'"
            )
            raise Exception("Invalid 'from' email password")

        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiverNumber, message)
        server.quit()
        return True
    except Exception as e:
        print("Error sending SMS: " + str(e))
        return False
