---
---

# 🦷 Dentist Office SMS Appointment System

An automated SMS appointment reminder and response handling system built with Python, Flask, and Twilio. This system sends appointment reminders to patients and allows them to confirm, reschedule, or cancel appointments via SMS responses.

## 📋 Features

- **Automated Appointment Reminders**: Sends SMS reminders 24 hours before appointments
- **Patient Response Handling**: Processes confirmation, reschedule, and cancellation requests
- **Two-Way SMS Communication**: Patients can interact with the system via text messages
- **Reschedule Options**: Provides available time slots when patients request reschedules
- **Web Dashboard**: View all appointments and system status
- **Webhook Integration**: Uses ngrok for local development and testing
- **Persistent Storage**: JSON-based appointment storage (easily upgradeable to database)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd dentist_sms_system

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your credentials
```
Required environment variables:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
OFFICE_NAME=Your Dental Office
OFFICE_PHONE=+1234567890
```

**Variable descriptions**

| Variable | Purpose |
|----------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio account identifier used for API calls. |
| `TWILIO_AUTH_TOKEN` | Authentication token paired with the SID. |
| `TWILIO_PHONE_NUMBER` | Twilio number that sends appointment reminders. |
| `OFFICE_NAME` | Name of the dental practice shown in messages. |
| `OFFICE_PHONE` | Contact phone number displayed to patients. |

### 3. Get Twilio Credentials

1. Sign up at [twilio.com](https://www.twilio.com)
2. Go to [Twilio Console](https://console.twilio.com)
3. Copy your Account SID and Auth Token
4. Purchase a phone number

### 4. Run the System

```bash
# Start the Flask server
python app.py
```

### 5. Expose with ngrok

```bash
# In another terminal
ngrok http 5000
```

### 6. Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Phone Numbers → Manage → Active numbers
3. Click on your Twilio number
4. Set webhook URL to: `https://your-ngrok-url.ngrok.io/webhook/sms`
5. Set HTTP method to `POST`

## 📱 Patient SMS Commands

Patients can respond to appointment reminders with:

| Command | Action |
|---------|--------|
| `CONFIRM` or `YES` | Confirm the appointment |
| `RESCHEDULE` or `CHANGE` | Request to reschedule |
| `CANCEL` or `NO` | Cancel the appointment |
| `1-5` | Select a reschedule option (after requesting reschedule) |

## 🌐 API Endpoints

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard with appointment overview |
| `POST` | `/webhook/sms` | Main SMS webhook (set in Twilio) |
| `GET/POST` | `/webhook/test` | Test webhook functionality |
| `POST` | `/send-reminders` | Manually trigger reminders |
| `GET` | `/appointments` | View all appointments (JSON) |
| `POST` | `/add-appointment` | Add new appointment |

### Example API Usage

#### Add Appointment
```bash
curl -X POST http://localhost:5000/add-appointment \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "APT004",
    "patient_name": "Alice Johnson",
    "patient_phone": "+1555123456",
    "appointment_date": "2024-01-15",
    "appointment_time": "14:00",
    "service": "Teeth Cleaning"
  }'
```

#### Trigger Reminders
```bash
curl -X POST http://localhost:5000/send-reminders
```

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Twilio SMS    │───▶│  Flask Webhook   │───▶│  Appointment    │
│    Gateway      │    │     Server       │    │    Manager      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   SMS Service    │
                       │  (Send/Receive)  │
                       └──────────────────┘
```

### Core Components

1. **`appointment_manager.py`**: Handles appointment storage and operations
2. **`sms_service.py`**: Manages Twilio SMS sending and response processing
3. **`app.py`**: Flask web server with webhook endpoints
4. **`appointments.json`**: Persistent storage for appointment data

## 📊 Sample Messages

### Appointment Reminder
```
🦷 Sunny Dental Care Reminder

Hi John Smith!

You have an appointment for Cleaning tomorrow (Monday, January 15, 2024 at 10:00 AM).

Please reply:
• CONFIRM to confirm your appointment
• RESCHEDULE to change the date/time
• CANCEL to cancel your appointment

Questions? Call us at +1234567890
```

### Reschedule Options
```
📅 Reschedule Request Received

Current appointment: Cleaning on Monday, January 15, 2024 at 10:00 AM

Available slots:
1. Tuesday, 01/16 at 09:00 AM
2. Tuesday, 01/16 at 02:00 PM
3. Wednesday, 01/17 at 11:00 AM
4. Thursday, 01/18 at 10:00 AM
5. Friday, 01/19 at 03:00 PM

Reply with the number (1-5) of your preferred slot, or call us for more options.

Call: +1234567890
```

## 🔧 Configuration Options

### Office Hours
Modify in `appointment_manager.py`:
```python
all_slots = [
    "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00", "17:00"
]
```

### Reminder Schedule
Modify in `app.py`:
```python
schedule.every().day.at("09:00").do(sms_service.send_bulk_reminders)
```

### Message Templates
Customize messages in `sms_service.py` methods:
- `_create_reminder_message()`
- `_handle_confirmation()`
- `_handle_reschedule_request()`
- `_handle_cancellation()`

## 🧪 Testing

### Test SMS Processing
```bash
# Test appointment reminder creation
python appointment_manager.py

# Test SMS service
python sms_service.py

# Test webhook with curl
curl -X POST http://localhost:5000/webhook/test
```

### Simulate Patient Responses
```bash
# Test confirmation
curl -X POST http://localhost:5000/webhook/sms \
  -d "From=+1234567890&Body=CONFIRM"

# Test reschedule request
curl -X POST http://localhost:5000/webhook/sms \
  -d "From=+1234567890&Body=RESCHEDULE"
```

## 📈 Production Deployment

### Database Upgrade
Replace JSON storage with PostgreSQL/MySQL:

```python
# In appointment_manager.py
import psycopg2
# Replace file operations with database queries
```

### Environment Variables
Set production environment variables:
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
FLASK_ENV=production
```

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **AWS EC2**: Full control with RDS database
- **DigitalOcean**: Simple deployment with managed database
- **Railway**: Modern deployment platform

## 🛡️ Security Considerations

- **Webhook Validation**: Verify Twilio signatures in production
- **Rate Limiting**: Implement rate limits for API endpoints  
- **Data Encryption**: Encrypt sensitive patient data
- **HTTPS Only**: Use SSL certificates in production
- **Access Control**: Implement authentication for admin endpoints

## 🐛 Troubleshooting

### Common Issues

1. **SMS not sending**: Check Twilio credentials and phone number format
2. **Webhook not receiving**: Verify ngrok URL and Twilio configuration
3. **Appointments not saving**: Check file permissions for `appointments.json`
4. **Reminder scheduling**: Ensure scheduler thread is running

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Files
Monitor application logs:
```bash
tail -f app.log
```

## 📚 Extensions

### Possible Enhancements
- Email notifications alongside SMS
- Multi-language support
- Insurance verification integration
- Payment reminders
- Automated follow-up surveys
- Integration with practice management software

### Advanced Features
- AI-powered appointment scheduling
- Voice call reminders
- WhatsApp integration
- Calendar synchronization
- Analytics dashboard

## 📄 License

This project is created for educational purposes. Feel free to use and modify for your dental practice needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

**Made with 🦷 for better dental practice management** 
