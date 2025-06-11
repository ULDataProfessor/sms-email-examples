# 🍽️ Restaurant Reservation Example

This example simulates taking a reservation for a restaurant. When you run `reservation_system.py` it gathers the guest's contact details, emails a confirmation, and sends a reminder text.

## How It Works
1. The script asks for the guest name, phone number, email address, and reservation time.
2. An email confirmation is sent using your SMTP settings.
3. A Twilio SMS reminder is sent on the day of the reservation.

## Environment Variables
After copying `env_example.txt` to `.env`, set the following:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID for sending SMS. |
| `TWILIO_AUTH_TOKEN` | Auth token for the Twilio account. |
| `TWILIO_PHONE_NUMBER` | Twilio number used to send reminders. |
| `EMAIL_HOST` | SMTP server to send emails. |
| `EMAIL_PORT` | Port number for the SMTP server. |
| `EMAIL_USE_TLS` | Set to `True` if SMTP requires TLS. |
| `EMAIL_USERNAME` | Username or address for SMTP authentication. |
| `EMAIL_PASSWORD` | Password or app password for SMTP. |
| `COMPANY_NAME` | Restaurant name displayed in messages. |
| `COMPANY_EMAIL` | Sender address for the confirmation email. |

## Run It
```bash
pip install -r requirements.txt
python reservation_system.py
```
