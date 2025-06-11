---
---

# 🚜 Farm Irrigation Alerts

Designed for a farm near Lethbridge, Alberta, this example triggers an SMS and email when soil moisture levels drop too low. Run `irrigation_alerts.py` and enter the current moisture reading to see it in action.

## Steps
1. Enter the phone number and email for the farmer.
2. Provide the field identifier and soil moisture percentage.
3. If moisture is under 25%, a warning is sent via Twilio and email.

### Snippet
```python
if moisture < 25:
    msg = f"Irrigation needed in {field}! Moisture at {moisture}%."
    send_sms(phone, msg)
    send_email(email, "Irrigation Alert", msg)
```

## Environment Variables
Copy `env_example.txt` to `.env` and set:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID. |
| `TWILIO_AUTH_TOKEN` | Twilio auth token. |
| `TWILIO_PHONE_NUMBER` | Number that sends SMS. |
| `EMAIL_HOST` | SMTP server address. |
| `EMAIL_PORT` | SMTP port. |
| `EMAIL_USE_TLS` | Use TLS (`True`/`False`). |
| `EMAIL_USERNAME` | SMTP username. |
| `EMAIL_PASSWORD` | SMTP password. |
| `FARM_EMAIL` | Sender address for email alerts. |

## Usage
```bash
pip install -r requirements.txt
python irrigation_alerts.py
```
