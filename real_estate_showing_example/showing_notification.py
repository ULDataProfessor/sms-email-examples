"""Real estate showing notification via email and SMS."""

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
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "agent@example.com")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Best Realty")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_email(to_addr: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = f"{COMPANY_NAME} <{COMPANY_EMAIL}>"
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
    client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number,
    )


def main() -> None:
    print("=== Schedule a Property Showing ===")
    phone = input("Buyer phone (+1...): ")
    email = input("Buyer email: ")
    address = input("Property address: ")
    when = input("Showing date/time: ")

    email_subject = f"Showing Scheduled for {address}"
    email_body = (
        f"Hi, your showing at {address} is scheduled for {when}. "
        f"Please reply if you need to reschedule."
    )
    send_email(email, email_subject, email_body)
    print("Confirmation email sent.")

    sms_text = f"Reminder: showing at {address} on {when}."
    send_sms(phone, sms_text)
    print("SMS reminder sent.")


if __name__ == "__main__":
    main()
