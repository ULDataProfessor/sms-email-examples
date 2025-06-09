# Twilio Python Teaching Examples

This repository contains multiple Python examples for teaching Twilio SMS functionality. These examples progress from basic to advanced concepts, perfect for classroom instruction.

## 📋 Prerequisites

- Python 3.7+
- Twilio Account (sign up at [twilio.com](https://www.twilio.com))
- Twilio Phone Number

## 🚀 Quick Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `env_example.txt` to `.env`
   - Fill in your Twilio credentials from the [Twilio Console](https://console.twilio.com)

   ```bash
   cp env_example.txt .env
   ```

   Edit `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890
   ```

## 📚 Examples Overview

### 1. Simple SMS Sender (`example_1_simple_sms.py`)
**Learning Goals:** Basic Twilio API usage, environment variables, error handling

**Features:**
- Send a simple SMS message
- Basic error handling
- Environment variable configuration

**Run:**
```bash
python example_1_simple_sms.py
```

### 2. Interactive Menu (`example_2_interactive_menu.py`)
**Learning Goals:** Menu-driven applications, different message types, user interaction

**Features:**
- Interactive command-line menu
- Multiple message types (quotes, facts, custom)
- User-friendly interface with emojis

**Run:**
```bash
python example_2_interactive_menu.py
```

### 3. Bulk SMS Sender (`example_3_bulk_sms.py`)
**Learning Goals:** Batch processing, rate limiting, error handling at scale

**Features:**
- Send messages to multiple recipients
- Personalized messages with templates
- Rate limiting and error tracking
- Detailed reporting

**Run:**
```bash
python example_3_bulk_sms.py
```

### 4. Webhook Receiver (`example_4_webhook_receiver.py`)
**Learning Goals:** Webhooks, incoming messages, auto-replies, Flask web server

**Features:**
- Receive incoming SMS messages
- Handle delivery status callbacks
- Auto-reply functionality
- Web dashboard

**Run:**
```bash
python example_4_webhook_receiver.py
```

### 5. Web Application (`main.py`)
**Learning Goals:** Full web application, APIs integration, user interface

**Features:**
- Web-based SMS sender
- Integration with external APIs (jokes, advice)
- Bootstrap UI
- Success/error handling

**Run:**
```bash
python main.py
```

### Additional Business Scenarios
The repository also includes extra examples that mix email and SMS:
1. **Monthly Box Order** (`monthly_box_example/`)
2. **Car Service Reminder** (`car_service_example/`)
3. **Event Registration** (`event_registration_example/`)
4. **Support Ticket Notifier** (`support_ticket_example/`)
5. **Restaurant Reservation** (`restaurant_reservation_example/`)

## 🔧 Configuration Details

### Environment Variables
All examples use the following environment variables:

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token  
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number (in E.164 format)

### Getting Twilio Credentials

1. Sign up at [twilio.com](https://www.twilio.com)
2. Go to the [Twilio Console](https://console.twilio.com)
3. Find your Account SID and Auth Token on the dashboard
4. Purchase a phone number from the Phone Numbers section

## 📖 Teaching Guide

### Lesson 1: Introduction to Twilio (30 minutes)
- What is Twilio?
- Setting up accounts and getting credentials
- Run `example_1_simple_sms.py`
- Discuss API basics and authentication

### Lesson 2: Building Interactive Applications (45 minutes)
- User input and validation
- Menu-driven programming
- Run `example_2_interactive_menu.py`
- Discuss code organization and user experience

### Lesson 3: Scaling SMS Operations (60 minutes)
- Batch processing concepts
- Error handling strategies
- Rate limiting and best practices
- Run `example_3_bulk_sms.py`
- Discuss production considerations

### Lesson 4: Webhooks and Two-Way Communication (60 minutes)
- What are webhooks?
- Setting up Flask servers
- Handling incoming messages
- Run `example_4_webhook_receiver.py`
- Use ngrok for local testing

### Lesson 5: Full Web Application (45 minutes)
- Web applications with Flask
- API integration
- User interface design
- Run `main.py`
- Discuss deployment considerations

## 🌐 Webhook Testing with ngrok

For testing webhooks locally:

1. Install ngrok: https://ngrok.com/download
2. Run your webhook server: `python example_4_webhook_receiver.py`
3. In another terminal: `ngrok http 5000`
4. Use the ngrok URL in your Twilio Console webhook settings

## 🐛 Troubleshooting

### Common Issues:

1. **Authentication Error**: Check your Account SID and Auth Token
2. **Phone Number Format**: Use E.164 format (+1234567890)
3. **Rate Limiting**: Add delays between bulk messages
4. **Webhook Issues**: Ensure your server is publicly accessible

### Error Messages:
- `Missing required Twilio credentials`: Check your `.env` file
- `Unable to reach webhook URL`: Verify ngrok is running for local testing
- `Invalid phone number`: Ensure numbers are in E.164 format

## 📝 Additional Resources

- [Twilio Python SDK Documentation](https://www.twilio.com/docs/libraries/python)
- [Twilio SMS API Reference](https://www.twilio.com/docs/sms/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ngrok Documentation](https://ngrok.com/docs)

## 🎯 Next Steps

After completing these examples, students can explore:
- Voice calls with Twilio
- WhatsApp Business API
- Twilio Flex for contact centers
- Twilio SendGrid for email
- Building chatbots with Twilio Studio

## Repository Notes
- Added a working email demo in `email_system/`
- Filled the empty requirements in `callmebot_whatsapp_example`

## 📄 License

This project is created for educational purposes. Feel free to use and modify for your teaching needs.

---

**Happy Teaching! 🎓📱** 