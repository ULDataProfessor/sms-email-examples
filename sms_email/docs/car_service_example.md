---
---

# 🚗 Car Service Reminder

This example simulates an auto shop that collects customer contact details and a service date. It sends an email confirmation immediately and schedules an SMS reminder before the appointment.

## How It Works
1. The script prompts for the customer's phone number, email, and desired service date.
2. An email confirmation is sent using the SMTP settings from your `.env` file.
3. A text reminder is then delivered to the customer's phone.

### Sending the Reminder
```python
sms_text = f"Reminder: your car service on {date} at {COMPANY_NAME}."
send_sms(phone, sms_text)
```

## Environment Variables
Create a `.env` file from `env_example.txt` and provide these values:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio account SID used to authenticate API calls. |
| `TWILIO_AUTH_TOKEN` | Auth token paired with the SID. |
| `TWILIO_PHONE_NUMBER` | Twilio phone number that sends reminders. |
| `EMAIL_HOST` | SMTP server address (e.g., `smtp.gmail.com`). |
| `EMAIL_PORT` | Port for the SMTP server. |
| `EMAIL_USE_TLS` | `True` if the server requires TLS. |
| `EMAIL_USERNAME` | Username or email address for SMTP authentication. |
| `EMAIL_PASSWORD` | Password or app password for SMTP authentication. |
| `COMPANY_NAME` | Name displayed in confirmation messages. |
| `COMPANY_EMAIL` | Sender address for confirmation emails. |

## Running
```bash
pip install -r requirements.txt
python service_reminder.py
```
Follow the prompts to schedule a reminder.
