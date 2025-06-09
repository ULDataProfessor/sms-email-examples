"""Car service appointment reminder example."""

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
COMPANY_NAME = os.getenv("COMPANY_NAME", "Auto Service Center")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "noreply@example.com")


def send_email(to_addr: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = COMPANY_EMAIL
    msg["To"] = to_addr
    msg.set_content(body)
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


def send_sms(number: str, text: str) -> None:
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(body=text, from_=os.getenv("TWILIO_PHONE_NUMBER"), to=number)


def main():
    print("=== Schedule Car Service ===")
    phone = input("Customer phone (+1...): ")
    email = input("Customer email: ")
    date = input("Appointment date (YYYY-MM-DD): ")

    email_subject = f"{COMPANY_NAME} Appointment Confirmation"
    email_body = f"Your car service is scheduled for {date}."
    send_email(email, email_subject, email_body)
    print("Email confirmation sent.")

    sms_text = f"Reminder: your car service on {date} at {COMPANY_NAME}."
    send_sms(phone, sms_text)
    print("SMS reminder sent.")


if __name__ == "__main__":
    main()
