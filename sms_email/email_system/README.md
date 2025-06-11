# 📧 Simple Email Sending System

This minimal Flask app demonstrates sending email through an SMTP server. When you visit the web page and enter an address, the app sends a welcome email.

## Setup
1. Copy `env_example.txt` to `.env` and fill in your SMTP settings.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5001` in your browser and submit your email address to test it.

## Environment Variables
The application expects these values in your `.env` file:

| Variable | Description |
|----------|-------------|
| `EMAIL_HOST` | SMTP server address (e.g., `smtp.gmail.com`). |
| `EMAIL_PORT` | Port for your SMTP server. |
| `EMAIL_USE_TLS` | `True` if the server requires TLS. |
| `EMAIL_USERNAME` | Username or email used to authenticate. |
| `EMAIL_PASSWORD` | Password or app password for your email account. |
| `COMPANY_NAME` | Name displayed in outgoing emails. |
| `COMPANY_EMAIL` | Address used as the sender. |
| `COMPANY_WEBSITE` | Website link included in the email footer. |
| `SUPPORT_EMAIL` | Contact address for support inquiries. |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions. |
| `FLASK_PORT` | Port number for running the app. |
