"""Clinic follow-up instructions by email and SMS."""

import os
from email.message import EmailMessage
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
CLINIC_EMAIL = os.getenv("CLINIC_EMAIL", "clinic@example.com")
CLINIC_NAME = os.getenv("CLINIC_NAME", "Downtown Clinic")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_email(to_addr: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = f"{CLINIC_NAME} <{CLINIC_EMAIL}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if EMAIL_USE_TLS:
            server.starttls()
        if EMAIL_USERNAME:
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


def send_sms(to_number: str, body: str) -> None:
    client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=to_number)


def main() -> None:
    print("=== Send Follow-Up Instructions ===")
    phone = input("Patient phone (+1...): ")
    email = input("Patient email: ")
    procedure = input("Procedure name: ")

    instructions = f"Thank you for visiting. Here are your {procedure} instructions."
    send_email(email, f"{procedure} Follow-Up", instructions)
    print("Follow-up email sent.")

    sms_text = f"We emailed your {procedure} instructions. Stay well!"
    send_sms(phone, sms_text)
    print("SMS confirmation sent.")


if __name__ == "__main__":
    main()
