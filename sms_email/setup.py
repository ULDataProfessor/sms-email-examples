#!/usr/bin/env python3
"""
Setup script for Twilio Python Teaching Examples
This script helps configure the environment for the first time.
"""

import os
import shutil


def create_env_file():
    """Create .env file from template"""
    env_example = "env_example.txt"
    env_file = ".env"

    if os.path.exists(env_file):
        overwrite = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != "y":
            print("Skipping .env file creation.")
            return False

    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print(f"✅ Created {env_file} from {env_example}")
        return True
    else:
        print(f"❌ {env_example} not found!")
        return False


def get_twilio_credentials():
    """Prompt user for Twilio credentials"""
    print("\n🔧 Twilio Credential Setup")
    print("=" * 40)
    print("You'll need these from your Twilio Console:")
    print("https://console.twilio.com\n")

    account_sid = input("Enter your Twilio Account SID: ").strip()
    auth_token = input("Enter your Twilio Auth Token: ").strip()
    phone_number = input("Enter your Twilio Phone Number (+1234567890): ").strip()

    return account_sid, auth_token, phone_number


def update_env_file(account_sid, auth_token, phone_number):
    """Update .env file with actual credentials"""
    env_file = ".env"

    try:
        with open(env_file, "r") as f:
            content = f.read()

        # Replace placeholder values
        content = content.replace("your_account_sid_here", account_sid)
        content = content.replace("your_auth_token_here", auth_token)
        content = content.replace("+1234567890", phone_number)

        with open(env_file, "w") as f:
            f.write(content)

        print(f"✅ Updated {env_file} with your credentials")
        return True

    except Exception as e:
        print(f"❌ Error updating {env_file}: {e}")
        return False


def check_requirements():
    """Check if requirements.txt exists"""
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        print(f"✅ Found {req_file}")
        install = input("Install requirements now? (y/n): ")
        if install.lower() == "y":
            os.system("pip install -r requirements.txt")
        return True
    else:
        print(f"❌ {req_file} not found!")
        return False


def main():
    """Main setup function"""
    print("🚀 Twilio Python Teaching Examples Setup")
    print("=" * 50)

    # Check requirements
    check_requirements()

    # Create .env file
    if create_env_file():
        # Get credentials from user
        account_sid, auth_token, phone_number = get_twilio_credentials()

        if all([account_sid, auth_token, phone_number]):
            update_env_file(account_sid, auth_token, phone_number)
        else:
            print("❌ Missing credentials. Please edit .env file manually.")

    print("\n🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Make sure your .env file has correct Twilio credentials")
    print("2. Run any example: python example_1_simple_sms.py")
    print("3. Check README.md for detailed instructions")


if __name__ == "__main__":
    main()
