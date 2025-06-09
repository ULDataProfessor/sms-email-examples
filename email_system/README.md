# 📧 Simple Email Sending System

This example demonstrates how to send an email using SMTP with a minimal Flask application. Configure your email credentials in `.env` and run the app to send yourself a welcome email.

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
4. Visit `http://localhost:5001` in your browser, enter your email address, and you will receive a test message.
