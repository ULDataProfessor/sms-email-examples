"""
Example 1: Simple SMS Sender
This is the most basic example of sending an SMS with Twilio.
Perfect for introducing students to the Twilio API.
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_simple_sms():
    """Send a simple SMS message"""
    # Get Twilio credentials from environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    # Create Twilio client
    client = Client(account_sid, auth_token)

    # Get recipient number from user
    to_number = input("Enter recipient phone number (with country code): ")

    # Create and send message
    message = client.messages.create(
        body="Hello from Twilio! This is your first SMS.",
        from_=from_number,
        to=to_number,
    )

    print("Message sent successfully!")
    print(f"Message SID: {message.sid}")
    print(f"Status: {message.status}")


if __name__ == "__main__":
    try:
        send_simple_sms()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set up your .env file with " "Twilio credentials!")
