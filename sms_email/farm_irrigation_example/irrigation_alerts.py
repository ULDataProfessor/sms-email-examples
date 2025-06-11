"""Farm irrigation monitoring for Lethbridge, Alberta."""

import os
from twilio.rest import Client
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
FARM_EMAIL = os.getenv("FARM_EMAIL", "farm@example.com")


def send_sms(to_number: str, body: str) -> None:
    client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=to_number)


def send_email(to_addr: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = FARM_EMAIL
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if EMAIL_USE_TLS:
            server.starttls()
        if EMAIL_USERNAME:
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


def main() -> None:
    print("=== Lethbridge Irrigation Alert ===")
    phone = input("Farmer phone (+1...): ")
    email = input("Farmer email: ")
    field = input("Field name/number: ")
    moisture = float(input("Current soil moisture (%): "))

    if moisture < 25:
        msg = f"Irrigation needed in {field}! Moisture at {moisture}%."
        send_sms(phone, msg)
        send_email(email, "Irrigation Alert", msg)
        print("Alerts sent for low moisture.")
    else:
        print("Moisture level adequate; no alerts sent.")


if __name__ == "__main__":
    main()
