"""
Example 2: Interactive SMS Menu
This example shows how to create a menu-driven SMS application.
Students can choose different message types to send.
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv
import random

load_dotenv()


class SMSMenu:
    """Interactive SMS menu system"""

    def __init__(self):
        self.client = self._setup_client()
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")

    def _setup_client(self):
        """Set up Twilio client"""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        return Client(account_sid, auth_token)

    def get_motivational_quote(self):
        """Get a random motivational quote"""
        quotes = [
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Success is not final, failure is not fatal. - Winston Churchill",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
        ]
        return random.choice(quotes)

    def get_fun_fact(self):
        """Get a random fun fact"""
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
            "A group of flamingos is called a 'flamboyance'.",
            "Bananas are berries, but strawberries aren't!",
            "A shrimp's heart is in its head.",
            "It rains diamonds on Saturn and Jupiter.",
        ]
        return random.choice(facts)

    def send_message(self, message, to_number):
        """Send SMS message"""
        try:
            message_obj = self.client.messages.create(
                body=message, from_=self.from_number, to=to_number
            )
            print(f"✅ Message sent! SID: {message_obj.sid}")
            return True
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("🚀 TWILIO SMS MENU")
        print("=" * 50)
        print("1. Send Motivational Quote")
        print("2. Send Fun Fact")
        print("3. Send Custom Message")
        print("4. Send Emergency Alert (Demo)")
        print("5. Exit")
        print("=" * 50)

    def run(self):
        """Run the interactive menu"""
        print("Welcome to the Twilio SMS Menu!")

        # Get recipient number once
        to_number = input("Enter recipient phone number (with country code): ")

        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                quote = self.get_motivational_quote()
                message = f"💪 Daily Motivation:\n\n{quote}"
                self.send_message(message, to_number)

            elif choice == "2":
                fact = self.get_fun_fact()
                message = f"🤔 Fun Fact:\n\n{fact}"
                self.send_message(message, to_number)

            elif choice == "3":
                custom_msg = input("Enter your custom message: ")
                self.send_message(custom_msg, to_number)

            elif choice == "4":
                alert_msg = "🚨 DEMO ALERT: This is a test emergency notification. Please respond with 'OK' to confirm receipt."
                self.send_message(alert_msg, to_number)

            elif choice == "5":
                print("Thank you for using Twilio SMS Menu! 👋")
                break

            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        menu = SMSMenu()
        menu.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set up your .env file with " "Twilio credentials!")
