import smtplib
from Constants import EMAIL_ADDRESS, EMAIL_PASSWORD, CARRIERS

def SendSMS(receiver, carrier, message):
    try:
        receiver_number = f'{receiver}{CARRIERS[carrier]}'
        print("Receiver number: ", receiver_number)
        print("Email address: ", EMAIL_ADDRESS)
        if EMAIL_ADDRESS is None:
            print("Invalid 'from' email address. Set it by running: \n\texport EMAIL_ADDRESS='[your email address]'")
            raise Exception("Invalid 'from' email address")
        if EMAIL_PASSWORD is None:
            print("Invalid 'from' email password. Set it by running: \n\texport EMAIL_PASSWORD='[your email password]'")  
            raise Exception("Invalid 'from' email password")
            
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver_number, message)
        return True
    except Exception as e:
        print("Error sending SMS: " + str(e))
        return False