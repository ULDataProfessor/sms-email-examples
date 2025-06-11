"""Utility for sending onboarding emails via SendGrid or SMTP."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@example.com")


def send_email(to_email: str, subject: str, body: str) -> None:
    """Send an email using SendGrid if configured, otherwise SMTP."""
    if SENDGRID_API_KEY:
        message = Mail(from_email=FROM_EMAIL, to_emails=to_email, subject=subject, html_content=body)
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return

    if SMTP_SERVER and SMTP_USERNAME and SMTP_PASSWORD:
        msg = EmailMessage()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body, subtype="html")
        with smtplib.SMTP(SMTP_SERVER) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return

    raise EnvironmentError("No email configuration found")

