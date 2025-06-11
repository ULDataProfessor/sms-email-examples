import os
from twilio.rest import Client


def send_message(msg, number):
    """Send SMS message using Twilio"""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        raise ValueError("Missing required Twilio credentials in environment variables")

    client = Client(account_sid, auth_token)

    # Format the recipient number
    if not number.startswith("+"):
        number = f"+1{number}"

    message = client.messages.create(body=msg, from_=from_number, to=number)

    print(f"Message sent! SID: {message.sid}")
    return message.sid
