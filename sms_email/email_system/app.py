from flask import Flask, request, render_template_string
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Example Company")
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "noreply@example.com")


def send_email(subject: str, body: str, recipient: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = COMPANY_EMAIL
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        subject = f"Welcome to {COMPANY_NAME}!"
        body = (
            f"Thank you for signing up for updates from {COMPANY_NAME}.\n"
            "We are excited to have you!"
        )
        send_email(subject, body, email)
        return "<h2>Email sent successfully!</h2>"

    return render_template_string(
        """
        <h1>Email Demo</h1>
        <form method='post'>
            <label>Email:</label>
            <input name='email' type='email' required>
            <button type='submit'>Send</button>
        </form>
        """
    )


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
