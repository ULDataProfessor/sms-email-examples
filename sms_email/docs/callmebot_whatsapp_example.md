---
---

# 📱 CallMeBot WhatsApp Example

This folder demonstrates how to send WhatsApp messages using the free [CallMeBot](https://www.callmebot.com/) API. It includes two scripts:

- `whatsapp_sender.py` – a helper class that sends messages through the CallMeBot API.
- `webhook_server.py` – a Flask application that exposes webhook endpoints and triggers WhatsApp notifications.

The example is designed for classroom use so students can experiment with WhatsApp automation without needing a Twilio WhatsApp account.

## How It Works
1. `whatsapp_sender.py` loads your credentials from `.env` and provides methods to send plain, emoji, or formatted messages.
2. `webhook_server.py` receives POST requests at `/webhook/*` and uses `WhatsAppSender` to deliver the messages.
3. You can run the server locally and expose it with ngrok for testing.

### Sending a Message
```python
sender = WhatsAppSender()
result = sender.send_message("Hello from CallMeBot!")
if result["success"]:
    print("Sent", result["phone"])
```

## Environment Variables
Create a `.env` file based on `env_example.txt` and set the following values:

| Variable | Description |
|----------|-------------|
| `WHATSAPP_PHONE_NUMBER` | Your WhatsApp number (country code, no `+`). |
| `CALLMEBOT_API_KEY` | API key obtained by messaging CallMeBot. |
| `WEBHOOK_SECRET` | Optional secret used to verify incoming webhook signatures. |

## Running the Demo
```bash
cd callmebot_whatsapp_example
pip install -r requirements.txt
python webhook_server.py
```
Visit `http://localhost:5000/webhook/test` to send a test message. Use `ngrok http 5000` if you want to receive webhooks from external services.
