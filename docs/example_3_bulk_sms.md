---
---

# Bulk SMS Sender

The script [example_3_bulk_sms.py](../example_3_bulk_sms.py) demonstrates sending personalized messages to a list of recipients.

```bash
python example_3_bulk_sms.py
```

It loops over phone numbers, sends each a message and prints the delivery status.

## Key Code
```python
class BulkSMSSender:
    def send_bulk_messages(self, contacts, message, delay=1):
        for contact in contacts:
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=contact,
            )
            time.sleep(delay)  # avoid hitting rate limits
```

You enter phone numbers one per line, then type the message once. The class sends to every number and reports how many succeeded or failed.
