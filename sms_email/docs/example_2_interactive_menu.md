---
---

# Interactive SMS Menu

`example_2_interactive_menu.py` shows how to build a simple menu-driven tool for sending different kinds of SMS messages.

```bash
python example_2_interactive_menu.py
```

Choose options like motivational quotes or fun facts and the script sends them via Twilio.

## Key Code
```python
class SMSMenu:
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def run(self):
        to_number = input("Enter recipient phone number: ")
        while True:
            print("1. Quote\n2. Fact\n3. Custom\n4. Exit")
            choice = input("Choose: ")
            if choice == "1":
                self.send_message(self.get_motivational_quote(), to_number)
            elif choice == "2":
                self.send_message(self.get_fun_fact(), to_number)
            elif choice == "3":
                msg = input("Your message: ")
                self.send_message(msg, to_number)
            else:
                break
```

The menu loops until the user exits, calling `send_message()` for each selection. It's a handy pattern for interactive SMS utilities.
