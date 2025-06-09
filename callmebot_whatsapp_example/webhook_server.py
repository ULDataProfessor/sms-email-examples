"""
CallMeBot WhatsApp Webhook Server
This Flask application receives webhook requests and sends WhatsApp messages
using the CallMeBot API.
"""

from flask import Flask, request, jsonify
import os
import hmac
import hashlib
from datetime import datetime
from whatsapp_sender import WhatsAppSender
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


class WebhookHandler:
    """Handle webhook requests and trigger WhatsApp messages"""

    def __init__(self):
        self.whatsapp = WhatsAppSender()
        self.webhook_secret = os.getenv("WEBHOOK_SECRET")

    def verify_signature(self, payload, signature):
        """Verify webhook signature for security"""
        if not self.webhook_secret or not signature:
            return True  # Skip verification if no secret is configured

        expected_signature = hmac.new(
            self.webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def process_webhook(self, data, webhook_type="generic"):
        """Process webhook data and send appropriate WhatsApp message"""
        try:
            if webhook_type == "alert":
                return self.handle_alert_webhook(data)
            elif webhook_type == "notification":
                return self.handle_notification_webhook(data)
            elif webhook_type == "status":
                return self.handle_status_webhook(data)
            else:
                return self.handle_generic_webhook(data)
        except Exception as e:
            return {"success": False, "error": f"Webhook processing failed: {str(e)}"}

    def handle_alert_webhook(self, data):
        """Handle alert-type webhooks"""
        title = data.get("title", "Alert")
        message = data.get("message", "An alert was triggered")
        severity = data.get("severity", "medium").upper()

        emoji_map = {"LOW": "🟡", "MEDIUM": "🟠", "HIGH": "🔴", "CRITICAL": "🚨"}

        emoji = emoji_map.get(severity, "⚠️")

        whatsapp_message = f"{emoji} *{severity} ALERT*\n\n"
        whatsapp_message += f"*{title}*\n\n"
        whatsapp_message += f"{message}\n\n"
        whatsapp_message += f"_Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"

        result = self.whatsapp.send_message(whatsapp_message)
        return result

    def handle_notification_webhook(self, data):
        """Handle notification-type webhooks"""
        title = data.get("title", "Notification")
        message = data.get("message", "You have a new notification")

        whatsapp_message = f"🔔 *Notification*\n\n"
        whatsapp_message += f"*{title}*\n\n"
        whatsapp_message += f"{message}\n\n"
        whatsapp_message += f"_Received: {datetime.now().strftime('%H:%M:%S')}_"

        result = self.whatsapp.send_message(whatsapp_message)
        return result

    def handle_status_webhook(self, data):
        """Handle status update webhooks"""
        service = data.get("service", "Unknown Service")
        status = data.get("status", "unknown")
        details = data.get("details", "")

        status_emoji = {"up": "✅", "down": "❌", "warning": "⚠️", "maintenance": "🔧"}

        emoji = status_emoji.get(status.lower(), "❓")

        whatsapp_message = f"{emoji} *Service Status Update*\n\n"
        whatsapp_message += f"*Service:* {service}\n"
        whatsapp_message += f"*Status:* {status.upper()}\n"

        if details:
            whatsapp_message += f"*Details:* {details}\n"

        whatsapp_message += (
            f"\n_Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
        )

        result = self.whatsapp.send_message(whatsapp_message)
        return result

    def handle_generic_webhook(self, data):
        """Handle generic webhooks"""
        message = data.get("message", str(data))

        whatsapp_message = f"📨 *Webhook Received*\n\n{message}\n\n"
        whatsapp_message += f"_Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"

        result = self.whatsapp.send_message(whatsapp_message)
        return result


# Initialize webhook handler
webhook_handler = WebhookHandler()


@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Main webhook endpoint for WhatsApp notifications"""
    try:
        # Get request data
        data = request.get_json() or {}
        signature = request.headers.get("X-Signature")

        # Verify signature if configured
        if not webhook_handler.verify_signature(request.data, signature):
            return jsonify({"success": False, "error": "Invalid signature"}), 401

        # Process the webhook
        result = webhook_handler.process_webhook(data, "generic")

        if result["success"]:
            return jsonify(
                {
                    "success": True,
                    "message": "WhatsApp message sent successfully",
                    "phone": result["phone"],
                }
            )
        else:
            return jsonify(result), 400

    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": f"Webhook processing failed: {str(e)}"}
            ),
            500,
        )


@app.route("/webhook/alert", methods=["POST"])
def alert_webhook():
    """Webhook endpoint for alerts"""
    try:
        data = request.get_json() or {}
        result = webhook_handler.process_webhook(data, "alert")

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/webhook/notification", methods=["POST"])
def notification_webhook():
    """Webhook endpoint for notifications"""
    try:
        data = request.get_json() or {}
        result = webhook_handler.process_webhook(data, "notification")

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/webhook/status", methods=["POST"])
def status_webhook():
    """Webhook endpoint for status updates"""
    try:
        data = request.get_json() or {}
        result = webhook_handler.process_webhook(data, "status")

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/webhook/test", methods=["GET", "POST"])
def test_webhook():
    """Test endpoint"""
    if request.method == "GET":
        return jsonify(
            {
                "status": "ok",
                "message": "CallMeBot WhatsApp Webhook Server is running!",
                "endpoints": [
                    "POST /webhook/whatsapp - Generic webhook",
                    "POST /webhook/alert - Alert notifications",
                    "POST /webhook/notification - General notifications",
                    "POST /webhook/status - Status updates",
                    "GET/POST /webhook/test - This test endpoint",
                ],
            }
        )
    else:
        # Test with sample data
        test_data = {"message": "This is a test webhook message from the server!"}
        result = webhook_handler.process_webhook(test_data)
        return jsonify(result)


@app.route("/")
def index():
    """Main page with webhook information"""
    return """
    <html>
    <head>
        <title>CallMeBot WhatsApp Webhook Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; }
            .example { background: #e8f4f8; padding: 15px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>📱 CallMeBot WhatsApp Webhook Server</h1>
        <p>This server receives webhooks and sends WhatsApp messages via CallMeBot API</p>
        
        <h2>🔗 Available Endpoints</h2>
        <div class="endpoint">
            <strong>POST /webhook/whatsapp</strong> - Generic webhook handler
        </div>
        <div class="endpoint">
            <strong>POST /webhook/alert</strong> - Alert notifications
        </div>
        <div class="endpoint">
            <strong>POST /webhook/notification</strong> - General notifications
        </div>
        <div class="endpoint">
            <strong>POST /webhook/status</strong> - Service status updates
        </div>
        <div class="endpoint">
            <strong>GET/POST /webhook/test</strong> - Test endpoint
        </div>
        
        <h2>📄 Example Payloads</h2>
        
        <h3>Alert Webhook:</h3>
        <div class="example">
            <code>
            {<br>
              &nbsp;&nbsp;"title": "Server Down",<br>
              &nbsp;&nbsp;"message": "Web server is not responding",<br>
              &nbsp;&nbsp;"severity": "high"<br>
            }
            </code>
        </div>
        
        <h3>Status Webhook:</h3>
        <div class="example">
            <code>
            {<br>
              &nbsp;&nbsp;"service": "Website",<br>
              &nbsp;&nbsp;"status": "down",<br>
              &nbsp;&nbsp;"details": "Connection timeout"<br>
            }
            </code>
        </div>
        
        <h2>🔧 Setup Instructions</h2>
        <ol>
            <li>Get your CallMeBot API key from <a href="https://wa.me/34644224527">https://wa.me/34644224527</a></li>
            <li>Send the message: "I allow callmebot to send me messages"</li>
            <li>Configure your .env file with phone number and API key</li>
            <li>Use ngrok for local testing: <code>ngrok http 5000</code></li>
        </ol>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("🚀 Starting CallMeBot WhatsApp Webhook Server...")
    print("📱 WhatsApp messages will be sent via CallMeBot API")
    print("\nAvailable endpoints:")
    print("  - POST /webhook/whatsapp (generic)")
    print("  - POST /webhook/alert (alerts)")
    print("  - POST /webhook/notification (notifications)")
    print("  - POST /webhook/status (status updates)")
    print("  - GET/POST /webhook/test (testing)")
    print("\n💡 Use ngrok to expose this server:")
    print("   ngrok http 5000")
    print("\n🔗 CallMeBot setup: https://wa.me/34644224527")

    app.run(host="0.0.0.0", port=5000, debug=True)
