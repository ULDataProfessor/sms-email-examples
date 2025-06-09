"""Support ticket notification example."""

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
COMPANY_NAME = os.getenv("COMPANY_NAME", "Support Desk")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "support@example.com")
SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "+10000000000")


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
    print("=== Create Support Ticket ===")
    customer_phone = input("Customer phone (+1...): ")
    customer_email = input("Customer email: ")
    issue = input("Brief issue description: ")

    email_subject = f"Ticket Received - {COMPANY_NAME}"
    email_body = (
        f"We received your support ticket: '{issue}'.\n"
        f"Our team will contact you shortly."
    )
    send_email(customer_email, email_subject, email_body)
    print("Confirmation email sent.")

    sms_text = f"Support ticket received: '{issue}'. We'll be in touch."
    send_sms(customer_phone, sms_text)
    print("SMS confirmation sent.")

    staff_subject = "New Support Ticket"
    staff_body = f"Ticket from {customer_email} / {customer_phone}: {issue}"
    send_email(COMPANY_EMAIL, staff_subject, staff_body)
    print("Staff notified.")


if __name__ == "__main__":
    main()
