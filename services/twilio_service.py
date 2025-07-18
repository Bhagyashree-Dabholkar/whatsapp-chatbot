import os
from twilio.rest import Client
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_SANDBOX_NUMBER')

client = Client(account_sid, auth_token)

def send_whatsapp_message(body, to):
    message = client.messages.create(
        from_=twilio_number,
        body=body,
        to=to
    )
    return message.sid
