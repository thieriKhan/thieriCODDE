from twilio.rest import Client



TWILIO_ACCOUNT_SID = 'AC970746d41c284fec2f46d5016f8e2f40'
TWILIO_AUTH_TOKEN = '6d14d3249378150ab957208ad35c5eaa'


def sendMessage(receiver, message):

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

# this is the Twilio sandbox testing number
    from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
    
    if receiver.startwith('6'):
        to_whatsapp_number2 = f'whatsapp:+237{receiver}'
    else :
        to_whatsapp_number2 = f'whatsapp:+2376{receiver}'
        to_whatsapp_number = f'whatsapp:+237{receiver}'


    client.messages.create(body=message,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
    
    client.messages.create(body= message,
                        from_ = from_whatsapp_number,
                        to=to_whatsapp_number)








# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
def  sendMedia(receiver, messag,url):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    to_whatsapp_number = f'whatsapp:+237{receiver}'
    client.messages \
        .create(
            media_url=[url],
            from_=messag,
            body="It's taco time!",
            to=to_whatsapp_number
        )

