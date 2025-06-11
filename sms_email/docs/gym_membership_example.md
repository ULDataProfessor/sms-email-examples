---
---

# 💪 Gym Membership Reminder

`membership_reminder.py` sends both an email and an SMS to members whose gym membership is about to expire. It's a simple way to automate renewal notices with Twilio.

## How It Works
1. Collect the member's contact details and renewal date.
2. Email them a friendly reminder to renew.
3. Text them the same information via SMS.

### Code Sample
```python
sms_text = f"Reminder: your {COMPANY_NAME} membership renews on {due_date}."
send_sms(phone, sms_text)
```

## Environment Variables
Copy `env_example.txt` to `.env` and set these values:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio account SID. |
| `TWILIO_AUTH_TOKEN` | Twilio auth token. |
| `TWILIO_PHONE_NUMBER` | Number that sends SMS reminders. |
| `EMAIL_HOST` | SMTP server address. |
| `EMAIL_PORT` | Port for SMTP. |
| `EMAIL_USE_TLS` | `True` or `False` for TLS. |
| `EMAIL_USERNAME` | SMTP username. |
| `EMAIL_PASSWORD` | SMTP password. |
| `COMPANY_NAME` | Gym name used in messages. |
| `COMPANY_EMAIL` | Sender address for the email reminder. |

## Usage
```bash
pip install -r requirements.txt
python membership_reminder.py
```
