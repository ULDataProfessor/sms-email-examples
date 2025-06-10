---
---

# Simple SMS Sender

This page explains the basics of sending a text message with Twilio using [example_1_simple_sms.py](../example_1_simple_sms.py).

```bash
python example_1_simple_sms.py
```

The script loads your Twilio credentials from a `.env` file, prompts for a destination phone number and sends a friendly SMS.

## Key Code
```python
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
from_number = os.getenv("TWILIO_PHONE_NUMBER")

to_number = input("Enter recipient phone number (with country code): ")
message = client.messages.create(
    body="Hello from Twilio! This is your first SMS.",
    from_=from_number,
    to=to_number,
)
print("Message sent:", message.sid)
```

The `Client` object handles authentication and message sending. After you run the script, Twilio will deliver the SMS to the number you entered.
