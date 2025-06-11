"""
Example 3: Bulk SMS Sender
This example demonstrates sending SMS to multiple recipients.
Great for teaching batch processing and error handling.
"""

import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class BulkSMSSender:
    """Bulk SMS sending system"""

    def __init__(self):
        self.client = self._setup_client()
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def _setup_client(self):
        """Set up Twilio client"""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        return Client(account_sid, auth_token)

    def read_contacts_from_input(self):
        """Get contacts from user input"""
        contacts = []
        print("Enter phone numbers (one per line, press Enter twice to finish):")

        while True:
            number = input().strip()
            if not number:
                break
            contacts.append(number)

        return contacts

    def send_bulk_messages(self, contacts, message, delay=1):
        """Send message to multiple contacts with delay"""
        successful = 0
        failed = 0
        results = []

        print(f"Sending message to {len(contacts)} contacts...")
        print("-" * 50)

        for i, contact in enumerate(contacts, 1):
            try:
                print(f"Sending to {contact} ({i}/{len(contacts)})...")

                message_obj = self.client.messages.create(
                    body=message, from_=self.from_number, to=contact
                )

                results.append(
                    {"contact": contact, "status": "success", "sid": message_obj.sid}
                )

                successful += 1
                print(f"✅ Success - SID: {message_obj.sid}")

                # Add delay to avoid rate limiting
                if i < len(contacts):
                    time.sleep(delay)

            except Exception as e:
                results.append(
                    {"contact": contact, "status": "failed", "error": str(e)}
                )

                failed += 1
                print(f"❌ Failed: {e}")

        # Print summary
        print("-" * 50)
        print(f"📊 SUMMARY:")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📱 Total: {len(contacts)}")

        return results

    def send_personalized_messages(self, contacts_with_names, template):
        """Send personalized messages using a template"""
        results = []

        for contact_info in contacts_with_names:
            name = contact_info["name"]
            number = contact_info["number"]

            # Replace {name} placeholder in template
            personalized_message = template.replace("{name}", name)

            try:
                message_obj = self.client.messages.create(
                    body=personalized_message, from_=self.from_number, to=number
                )

                results.append(
                    {
                        "name": name,
                        "contact": number,
                        "status": "success",
                        "sid": message_obj.sid,
                    }
                )

                print(f"✅ Sent to {name} ({number})")

            except Exception as e:
                results.append(
                    {
                        "name": name,
                        "contact": number,
                        "status": "failed",
                        "error": str(e),
                    }
                )

                print(f"❌ Failed to send to {name}: {e}")

        return results

    def demo_bulk_sms(self):
        """Demo the bulk SMS functionality"""
        print("🚀 Bulk SMS Demo")
        print("=" * 30)

        # Get contacts
        contacts = self.read_contacts_from_input()

        if not contacts:
            print("No contacts provided. Exiting.")
            return

        # Get message
        message = input("Enter message to send to all contacts: ")

        # Send bulk messages
        results = self.send_bulk_messages(contacts, message)

        return results

    def demo_personalized_sms(self):
        """Demo personalized SMS functionality"""
        print("🎯 Personalized SMS Demo")
        print("=" * 30)

        # Example contacts with names
        contacts_with_names = [
            {"name": "Alice", "number": "+1234567890"},
            {"name": "Bob", "number": "+1987654321"},
        ]

        print("Demo will send to these contacts:")
        for contact in contacts_with_names:
            print(f"- {contact['name']}: {contact['number']}")

        # Template with placeholder
        template = "Hello {name}! This is a personalized message from Twilio."

        print(f"Using template: {template}")

        confirm = input("Send demo messages? (y/n): ")
        if confirm.lower() == "y":
            results = self.send_personalized_messages(contacts_with_names, template)
            return results
        else:
            print("Demo cancelled.")
            return []


def main():
    """Main function"""
    bulk_sender = BulkSMSSender()

    while True:
        print("\n" + "=" * 40)
        print("📱 BULK SMS EXAMPLES")
        print("=" * 40)
        print("1. Send same message to multiple contacts")
        print("2. Send personalized messages (demo)")
        print("3. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            bulk_sender.demo_bulk_sms()
        elif choice == "2":
            bulk_sender.demo_personalized_sms()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set up your .env file with " "Twilio credentials!")
