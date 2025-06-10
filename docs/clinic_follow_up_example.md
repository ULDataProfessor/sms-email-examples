---
---

# 🩺 Clinic Follow-Up Example

After a medical appointment, clinics often send instructions to patients. `follow_up_sender.py` emails the detailed instructions and sends a quick SMS letting the patient know to check their inbox.

## How It Works
1. Enter the patient's phone, email and procedure name.
2. The script emails follow-up instructions for that procedure.
3. It also sends a short confirmation text.

### Code Snippet
```python
instructions = f"Thank you for visiting. Here are your {procedure} instructions."
send_email(email, f"{procedure} Follow-Up", instructions)
send_sms(phone, "We emailed your instructions.")
```

## Environment Variables
Copy `env_example.txt` to `.env` and configure:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID. |
| `TWILIO_AUTH_TOKEN` | Twilio auth token. |
| `TWILIO_PHONE_NUMBER` | Number used for SMS notices. |
| `EMAIL_HOST` | SMTP host. |
| `EMAIL_PORT` | SMTP port. |
| `EMAIL_USE_TLS` | Use TLS (`True`/`False`). |
| `EMAIL_USERNAME` | SMTP username. |
| `EMAIL_PASSWORD` | SMTP password. |
| `CLINIC_EMAIL` | Sender address for follow-ups. |
| `CLINIC_NAME` | Clinic name used in messages. |

## Run It
```bash
pip install -r requirements.txt
python follow_up_sender.py
```
