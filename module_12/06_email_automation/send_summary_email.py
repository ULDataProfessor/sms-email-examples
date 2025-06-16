"""Send an email with summary.xlsx attached."""
from __future__ import annotations

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.example.com"
FROM_ADDR = "me@example.com"
ATTACHMENT = Path("summary.xlsx")


def send_email(recipients: list[str]) -> None:
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    msg = MIMEMultipart()
    msg["Subject"] = "Daily Summary"
    msg["From"] = FROM_ADDR
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText("See attached summary."))

    with open(ATTACHMENT, "rb") as f:
        part = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={ATTACHMENT.name}")
    msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, 587) as s:
        s.starttls()
        s.login(user, password)
        s.sendmail(FROM_ADDR, recipients, msg.as_string())


def main() -> None:
    recipients = os.getenv("RECIPIENTS", "").split(",")
    recipients = [r.strip() for r in recipients if r.strip()]
    if recipients:
        send_email(recipients)


if __name__ == "__main__":
    main()
