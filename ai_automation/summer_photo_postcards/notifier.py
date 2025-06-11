"""Send order confirmation emails."""

import os
import smtplib
from email.message import EmailMessage
from typing import Dict

from .config import logger
from .utils import NotificationError

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def send_confirmation(order: Dict[str, str]) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Your summer postcards order"
    msg["From"] = FROM_EMAIL
    msg["To"] = order["customer_email"]
    body = (
        f"Thanks {order['customer_name']}!\n"
        f"Order ID: {order['print_order_id']}\n"
        f"Track: {order.get('tracking_url', 'pending')}"
    )
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER) as smtp:
            smtp.starttls()
            if SMTP_USER:
                smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)
        logger.info("Confirmation email sent to %s", order["customer_email"])
    except Exception as exc:
        logger.error("Failed to send email: %s", exc)
        raise NotificationError(str(exc)) from exc
