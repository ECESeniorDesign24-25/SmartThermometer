from twilio.rest import Client
 
def SendText(receiver, message):
    account_sid = 'ACb33b1679ec3990ce81517cf08cffc5c6'
    auth_token = '[AuthToken]'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+18665094281',
    body='Hello from Twilio',
    to='+18777804236'
    )

    print(message.sid)