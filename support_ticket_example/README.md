# 🛠️ Support Ticket Notifier

This example mimics a help desk system. Running `ticket_notifier.py` prompts the user for their issue. The customer receives an email and SMS confirming the ticket, while the support team gets an email with the details.

## How It Works
1. The script collects the customer's name, phone number, and a brief description of the issue.
2. An email is sent to the customer and support team using your SMTP configuration.
3. A confirmation SMS is sent to the customer using Twilio.

## Environment Variables
Create `.env` from `env_example.txt` and configure these values:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID used for SMS. |
| `TWILIO_AUTH_TOKEN` | Twilio authentication token. |
| `TWILIO_PHONE_NUMBER` | Twilio number that sends confirmations. |
| `EMAIL_HOST` | SMTP server address. |
| `EMAIL_PORT` | SMTP server port. |
| `EMAIL_USE_TLS` | Whether the server requires TLS. |
| `EMAIL_USERNAME` | Username or address for SMTP login. |
| `EMAIL_PASSWORD` | Password or app password for SMTP. |
| `COMPANY_NAME` | Name of the support organization. |
| `COMPANY_EMAIL` | Email address used as the sender. |
| `SUPPORT_PHONE` | Phone number displayed in support emails. |

## Steps
```bash
pip install -r requirements.txt
python ticket_notifier.py
```
