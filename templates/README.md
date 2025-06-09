# 🗂️ Templates Folder

This directory contains HTML templates used by `main.py`. The `index.html` file provides a small form that allows a user to submit a phone number and receive a joke and a piece of advice via SMS.

The template relies on a few context variables passed from the Flask application:

| Variable | Purpose |
|----------|---------|
| `success` | Boolean flag indicating if the SMS was sent successfully. |
| `success_img` | URL for the success image displayed after sending. |
| `phone_number` | The number entered by the user in the form. |

No environment variables are required for the templates themselves, but the Flask app that renders them uses the Twilio credentials described in the main README.
