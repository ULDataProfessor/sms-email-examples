---
---

# 🎫 Event Registration Example

This folder contains a short script that mimics registering a user for an event. When `event_notifier.py` runs it asks for the attendee's contact information, sends a ticket via email, and texts them a reminder using Twilio.

## How It Works
1. User details are collected on the command line.
2. A confirmation email is sent through your SMTP server.
3. An SMS reminder is delivered to the attendee.

### Example Code
```python
email_subject = f"Your ticket for {event}"
email_body = "Thanks for registering!"
send_email(email, email_subject, email_body)

sms_text = f"Reminder: you're registered for {event}!"
send_sms(phone, sms_text)
```

## Environment Variables
Copy `env_example.txt` to `.env` and set these variables:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio account SID. |
| `TWILIO_AUTH_TOKEN` | Auth token for Twilio. |
| `TWILIO_PHONE_NUMBER` | Twilio number that sends the reminder. |
| `EMAIL_HOST` | Address of your SMTP server. |
| `EMAIL_PORT` | Port number for SMTP. |
| `EMAIL_USE_TLS` | Use TLS (`True` or `False`). |
| `EMAIL_USERNAME` | SMTP username or email. |
| `EMAIL_PASSWORD` | SMTP password or app password. |
| `COMPANY_NAME` | Name of the organization hosting the event. |
| `COMPANY_EMAIL` | Sender address for confirmation emails. |

## Usage
```bash
pip install -r requirements.txt
python event_notifier.py
```
