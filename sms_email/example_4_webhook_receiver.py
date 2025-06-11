"""
Example 4: Twilio Webhook Receiver
This example shows how to receive and handle incoming SMS messages
and delivery status callbacks from Twilio.
"""

from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/webhook/sms", methods=["POST"])
def receive_sms():
    """Handle incoming SMS messages"""
    # Get message data from Twilio
    from_number = request.form.get("From")
    to_number = request.form.get("To")
    message_body = request.form.get("Body")
    message_sid = request.form.get("MessageSid")

    print("📱 INCOMING SMS RECEIVED:")
    print(f"From: {from_number}")
    print(f"To: {to_number}")
    print(f"Message: {message_body}")
    print(f"SID: {message_sid}")
    print("-" * 50)

    # Process the message (you can add your logic here)
    response_message = process_incoming_message(message_body, from_number)

    # Send automatic response (optional)
    if response_message:
        return create_twiml_response(response_message)

    # Return empty TwiML to acknowledge receipt
    return "<Response></Response>"


@app.route("/webhook/status", methods=["POST"])
def message_status():
    """Handle message delivery status callbacks"""
    message_sid = request.form.get("MessageSid")
    message_status = request.form.get("MessageStatus")
    to_number = request.form.get("To")

    print("📊 MESSAGE STATUS UPDATE:")
    print(f"SID: {message_sid}")
    print(f"Status: {message_status}")
    print(f"To: {to_number}")
    print("-" * 50)

    # Log or process status update
    log_message_status(message_sid, message_status, to_number)

    return "<Response></Response>"


def process_incoming_message(message_body, from_number):
    """Process incoming message and return response if needed"""
    message_lower = message_body.lower().strip()

    # Auto-reply examples
    if message_lower == "hello":
        return "Hello! Thanks for messaging us. How can we help you today?"

    elif message_lower == "help":
        return (
            "Available commands:\n"
            "HELLO - Get a greeting\n"
            "TIME - Get current time\n"
            "JOKE - Get a random joke\n"
            "STOP - Unsubscribe"
        )

    elif message_lower == "time":
        from datetime import datetime

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Current time: {current_time}"

    elif message_lower == "joke":
        return "Why don't scientists trust atoms? Because they make up everything!"

    elif message_lower == "stop":
        return (
            "You have been unsubscribed from automated messages. "
            "Reply START to resubscribe."
        )

    # For demo purposes, echo back the message
    return f"You said: {message_body}"


def create_twiml_response(message):
    """Create TwiML response to send back to user"""
    return f"<Response><Message>{message}</Message></Response>"


def log_message_status(message_sid, status, to_number):
    """Log message delivery status"""
    # In a real application, you might save this to a database
    print(f"Logging: Message {message_sid} to {to_number} is {status}")


@app.route("/webhook/test", methods=["GET"])
def test_webhook():
    """Test endpoint to check if webhook server is running"""
    return {
        "status": "ok",
        "message": "Webhook server is running!",
        "endpoints": [
            "/webhook/sms - Handle incoming SMS",
            "/webhook/status - Handle delivery status",
            "/webhook/test - This test endpoint",
        ],
    }


@app.route("/")
def index():
    """Main page with webhook information"""
    return """
    <h1>Twilio Webhook Receiver</h1>
    <p>This server is ready to receive Twilio webhooks!</p>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><strong>/webhook/sms</strong> - Handle incoming SMS messages</li>
        <li><strong>/webhook/status</strong> - Handle delivery status callbacks</li>
        <li><strong>/webhook/test</strong> - Test endpoint</li>
    </ul>
    <h2>Setup Instructions:</h2>
    <ol>
        <li>Make sure this server is accessible from the internet (use ngrok for local development)</li>
        <li>In your Twilio Console, set your webhook URL to: <code>https://your-domain.com/webhook/sms</code></li>
        <li>For status callbacks, use: <code>https://your-domain.com/webhook/status</code></li>
    </ol>
    """


if __name__ == "__main__":
    print("🚀 Starting Twilio Webhook Receiver...")
    print("Available endpoints:")
    print("  - POST /webhook/sms (incoming messages)")
    print("  - POST /webhook/status (delivery status)")
    print("  - GET /webhook/test (test endpoint)")
    print("\n💡 Pro tip: Use ngrok to expose this server to the internet!")
    print("   ngrok http 5000")

    app.run(host="0.0.0.0", port=5000, debug=True)
