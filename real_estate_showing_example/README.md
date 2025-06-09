# 🏠 Real Estate Showing Example

This demo shows how a real estate agent might schedule property showings. When you run `showing_notification.py`, it collects the buyer's phone number, email address, property location and showing time. It then sends an email confirmation and an SMS reminder.

## How It Works
1. Prompt the agent for buyer contact details and showing info.
2. Send an email with the date, time and address of the showing.
3. Text the buyer a short reminder using Twilio.

## Environment Variables
Copy `env_example.txt` to `.env` and fill in the following values:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio account SID. |
| `TWILIO_AUTH_TOKEN` | Auth token for Twilio. |
| `TWILIO_PHONE_NUMBER` | Number that sends the SMS reminder. |
| `EMAIL_HOST` | SMTP server address. |
| `EMAIL_PORT` | SMTP server port. |
| `EMAIL_USE_TLS` | Whether to use TLS with SMTP. |
| `EMAIL_USERNAME` | Username or email for SMTP auth. |
| `EMAIL_PASSWORD` | Password or app password for SMTP. |
| `COMPANY_NAME` | Name used in messages. |
| `COMPANY_EMAIL` | Sender address for email confirmations. |

## Running
```bash
pip install -r requirements.txt
python showing_notification.py
```
