import smtplib
from email.message import EmailMessage
from Constants import EMAIL_ADDRESS, EMAIL_PASSWORD

def SendEmail(receiver, subject, body):
    try:
        print("Email address: ", EMAIL_ADDRESS)
        if EMAIL_ADDRESS is None:
            print("Invalid 'from' email address. Set it by running: \n\texport EMAIL_ADDRESS='[your email address]'")
            raise Exception("Invalid 'from' email address")
        if EMAIL_PASSWORD is None:
            print("Invalid 'from' email password. Set it by running: \n\texport EMAIL_PASSWORD='[your email password]'")  
            raise Exception("Invalid 'from' email password")

        msg = EmailMessage()
        msg.set_content(body)

        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver

        s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
        s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        print("Error sending email: " + str(e))
        return False