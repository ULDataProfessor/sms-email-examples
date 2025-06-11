"""Simple monthly box order notification example."""

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
COMPANY_NAME = os.getenv("COMPANY_NAME", "Monthly Box Co")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "noreply@example.com")


def send_email(recipient: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = COMPANY_EMAIL
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


def send_sms(number: str, message: str) -> None:
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    client.messages.create(body=message, from_=from_number, to=number)


def main():
    print("=== Monthly Box Order ===")
    phone = input("Customer phone (+1...): ")
    email = input("Customer email: ")

    email_subject = f"Thanks for your order from {COMPANY_NAME}"
    email_body = (
        f"Hi there! Your first subscription box will ship soon. "
        f"We'll notify you when it goes out."
    )
    send_email(email, email_subject, email_body)
    print("Email sent!")

    sms_message = "Your Monthly Box order was received! We'll text you when it ships."
    send_sms(phone, sms_message)
    print("SMS sent!")


if __name__ == "__main__":
    main()
