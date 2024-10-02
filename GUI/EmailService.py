import smtplib
from Receiver import Receiver
from email.message import EmailMessage
from Constants import EMAIL_ADDRESS, EMAIL_PASSWORD


def SendEmail(client_email: str, subject: str, message: str):
    """
    Sends an email to the given receiver email address
    """
    try:
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

        msg = EmailMessage()
        msg.set_content(message)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = client_email

        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
