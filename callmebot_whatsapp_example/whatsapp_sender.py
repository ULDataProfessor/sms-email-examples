"""
CallMeBot WhatsApp Message Sender
This module provides functionality to send WhatsApp messages using the free
CallMeBot API service.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WhatsAppSender:
    """WhatsApp message sender using CallMeBot API"""

    def __init__(self):
        self.phone_number = os.getenv("WHATSAPP_PHONE_NUMBER")
        self.api_key = os.getenv("CALLMEBOT_API_KEY")
        self.base_url = "https://api.callmebot.com/whatsapp.php"

        if not self.phone_number or not self.api_key:
            raise ValueError(
                "Missing WhatsApp credentials. Please check your .env file.\n"
                "Visit https://wa.me/34644224527 and send 'I allow callmebot "
                "to send me messages' to get your API key."
            )

    def send_message(self, message, to_phone=None):
        """
        Send WhatsApp message using CallMeBot API

        Args:
            message (str): Message to send
            to_phone (str, optional): Recipient phone number.
                                    If None, sends to configured number.

        Returns:
            dict: Response with success status and details
        """
        try:
            # Use provided phone number or default to configured one
            phone = to_phone or self.phone_number

            # Prepare parameters for the API call
            params = {"phone": phone, "text": message, "apikey": self.api_key}

            # Make the API request
            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                # Create preview text for response
                text_preview = message[:50] + "..." if len(message) > 50 else message
                return {
                    "success": True,
                    "message": "WhatsApp message sent successfully!",
                    "phone": phone,
                    "text": text_preview,
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "phone": phone,
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "phone": phone,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "phone": phone,
            }

    def send_emoji_message(self, message):
        """
        Send a WhatsApp message with emojis

        Args:
            message (str): Message with emoji codes

        Returns:
            dict: Response with success status and details
        """
        # CallMeBot supports emoji codes like :smile:, :heart:, etc.
        emoji_message = f"🤖 {message} 🚀"
        return self.send_message(emoji_message)

    def send_formatted_message(self, title, content, footer=None):
        """
        Send a formatted WhatsApp message

        Args:
            title (str): Message title
            content (str): Main content
            footer (str, optional): Footer text

        Returns:
            dict: Response with success status and details
        """
        formatted_message = f"*{title}*\n\n{content}"

        if footer:
            formatted_message += f"\n\n_{footer}_"

        return self.send_message(formatted_message)

    def test_connection(self):
        """
        Test the connection to CallMeBot API

        Returns:
            dict: Test result
        """
        test_message = "🧪 CallMeBot API Test - Connection successful!"
        result = self.send_message(test_message)

        if result["success"]:
            print("✅ CallMeBot API connection test successful!")
            print(f"📱 Message sent to: {result['phone']}")
        else:
            print("❌ CallMeBot API connection test failed!")
            print(f"Error: {result['error']}")

        return result


def main():
    """Demo function to test WhatsApp sending"""
    try:
        sender = WhatsAppSender()

        print("🔄 Testing CallMeBot WhatsApp API...")

        # Test basic message
        result = sender.test_connection()

        if result["success"]:
            print("\n📱 Sending additional test messages...")

            # Test emoji message
            sender.send_emoji_message("Hello from Python!")

            # Test formatted message
            sender.send_formatted_message(
                "API Test Results",
                "CallMeBot WhatsApp integration is working correctly!",
                "Sent from Python script",
            )

            print("✅ All test messages sent successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Setup instructions:")
        print("1. Copy env_example.txt to .env")
        print("2. Visit https://wa.me/34644224527")
        print("3. Send: 'I allow callmebot to send me messages'")
        print("4. Update .env with your phone number and API key")


if __name__ == "__main__":
    main()
