---
---

# Webhook Receiver

`example_4_webhook_receiver.py` starts a small Flask app that listens for incoming SMS messages and status callbacks.

```bash
python example_4_webhook_receiver.py
```

Use a tool like ngrok to expose the local server while testing.

## Key Code
```python
@app.route("/webhook/sms", methods=["POST"])
def receive_sms():
    from_number = request.form.get("From")
    body = request.form.get("Body")
    print(f"Message from {from_number}: {body}")
    return create_twiml_response("Thanks for texting!")
```

The Flask route prints the inbound message and replies using basic TwiML. Another route handles delivery status callbacks for outgoing messages.
