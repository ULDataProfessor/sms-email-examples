import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import List

import pandas as pd
from dotenv import load_dotenv

from logger import DB_PATH

load_dotenv()

SMTP_SERVER = os.environ.get("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")


def fetch_logs() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()
    return pd.read_sql("SELECT * FROM reorder_log", f"sqlite:///{DB_PATH}")


def build_message(forecast_df: pd.DataFrame, log_df: pd.DataFrame) -> str:
    reordered = log_df[log_df["success"] == 1]
    exceptions = log_df[log_df["success"] == 0]

    lines = ["Daily Inventory Auto-Reorder Report", ""]
    lines.append("Items reordered:")
    if not reordered.empty:
        for _, row in reordered.iterrows():
            lines.append(f"- {row['item_id']} qty {row['quantity']} status {row['status_code']}")
    else:
        lines.append("None")

    lines.append("\nPredicted stock-out dates:")
    for _, row in forecast_df.iterrows():
        lines.append(f"- {row['item_id']}: {row['stockout_date']}")

    if not exceptions.empty:
        lines.append("\nExceptions:")
        for _, row in exceptions.iterrows():
            lines.append(f"- {row['item_id']} error: {row['error']}")

    return "\n".join(lines)


def send_email(subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER or "noreply@example.com"
    msg["To"] = EMAIL_TO or ""

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if EMAIL_USER and EMAIL_PASS:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def send_daily_report(forecast_df: pd.DataFrame) -> None:
    logs = fetch_logs()
    message = build_message(forecast_df, logs)
    send_email("Cafe Inventory Report", message)

