# 📦 Monthly Box Order Example

This script simulates a customer subscribing to a monthly box. It collects the customer's phone number and email address, sends a confirmation email, and delivers a short SMS via Twilio.

## How It Works
1. The user enters their contact information when running `order_system.py`.
2. The script uses your SMTP settings to send an email confirmation.
3. A Twilio SMS is sent to let the customer know their first box is on the way.

## Environment Variables
Copy `env_example.txt` to `.env` and define the following:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID used for SMS. |
| `TWILIO_AUTH_TOKEN` | Twilio auth token. |
| `TWILIO_PHONE_NUMBER` | Number from which SMS notifications are sent. |
| `EMAIL_HOST` | SMTP server address. |
| `EMAIL_PORT` | SMTP server port. |
| `EMAIL_USE_TLS` | Whether to use TLS for SMTP. |
| `EMAIL_USERNAME` | Your email username or address. |
| `EMAIL_PASSWORD` | Password or app password for your email account. |
| `COMPANY_NAME` | Company name included in messages. |
| `COMPANY_EMAIL` | Email address used as the sender. |

## Running
```bash
pip install -r requirements.txt
python order_system.py
```
