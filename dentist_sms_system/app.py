"""
Dentist Office SMS Appointment System
Flask application with webhook endpoints for handling SMS responses via Twilio.
"""

from flask import Flask, request, render_template_string
import os
import threading
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from sms_service import sms_service
from appointment_manager import (
    appointment_manager,
    create_sample_appointments,
    Appointment,
)

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """Main dashboard showing appointment system status"""
    appointments = appointment_manager.get_all_appointments()
    tomorrow_appointments = appointment_manager.get_tomorrows_appointments()

    office_name = os.getenv("OFFICE_NAME", "Dental Office")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{office_name} - SMS Appointment System</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f7fa; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .appointment {{ padding: 10px; margin: 10px 0; border-left: 4px solid #3498db; background: #ecf0f1; }}
            .status-scheduled {{ border-left-color: #f39c12; }}
            .status-confirmed {{ border-left-color: #27ae60; }}
            .status-cancelled {{ border-left-color: #e74c3c; }}
            .stats {{ display: flex; gap: 20px; }}
            .stat {{ flex: 1; text-align: center; padding: 15px; background: #3498db; color: white; border-radius: 5px; }}
            .endpoint {{ background: #2c3e50; color: white; padding: 10px; margin: 5px 0; border-radius: 5px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🦷 {office_name}</h1>
            <h2>SMS Appointment System Dashboard</h2>
            <p>Automated appointment reminders and patient response handling</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <h3>{len(appointments)}</h3>
                <p>Total Appointments</p>
            </div>
            <div class="stat">
                <h3>{len(tomorrow_appointments)}</h3>
                <p>Tomorrow's Reminders</p>
            </div>
            <div class="stat">
                <h3>{len([a for a in appointments if a.status == 'confirmed'])}</h3>
                <p>Confirmed</p>
            </div>
            <div class="stat">
                <h3>{len([a for a in appointments if a.status == 'cancelled'])}</h3>
                <p>Cancelled</p>
            </div>
        </div>
        
        <div class="card">
            <h3>📱 SMS Webhook Endpoints</h3>
            <div class="endpoint">POST /webhook/sms - Main SMS webhook</div>
            <div class="endpoint">GET /webhook/test - Test endpoint</div>
            <div class="endpoint">POST /send-reminders - Manual reminder trigger</div>
            <div class="endpoint">GET /appointments - View all appointments</div>
        </div>
        
        <div class="card">
            <h3>📅 Upcoming Appointments</h3>
    """

    if appointments:
        for apt in sorted(appointments, key=lambda x: x.get_datetime()):
            if apt.status != "cancelled":
                status_class = f"status-{apt.status}"
                html += f"""
                <div class="appointment {status_class}">
                    <strong>{apt.patient_name}</strong> - {apt.service}<br>
                    📅 {apt.format_appointment_info()}<br>
                    📱 {apt.patient_phone} | Status: {apt.status.upper()}<br>
                    {'✅ Reminder sent' if apt.reminder_sent else '⏳ Reminder pending'}
                </div>
                """
    else:
        html += "<p>No appointments scheduled.</p>"

    html += """
        </div>
        
        <div class="card">
            <h3>🔧 Setup Instructions</h3>
            <ol>
                <li>Configure your .env file with Twilio credentials</li>
                <li>Start the Flask server: <code>python app.py</code></li>
                <li>Start ngrok: <code>ngrok http 5000</code></li>
                <li>Set Twilio webhook URL to: <code>https://your-ngrok-url.ngrok.io/webhook/sms</code></li>
                <li>Test with sample appointments or add your own</li>
            </ol>
        </div>
        
        <div class="card">
            <h3>📝 Patient Commands</h3>
            <p>Patients can reply to appointment reminders with:</p>
            <ul>
                <li><strong>CONFIRM</strong> - Confirm the appointment</li>
                <li><strong>RESCHEDULE</strong> - Request to change date/time</li>
                <li><strong>CANCEL</strong> - Cancel the appointment</li>
                <li><strong>1-5</strong> - Select a reschedule option (after requesting reschedule)</li>
            </ul>
        </div>
    </body>
    </html>
    """

    return html


@app.route("/webhook/sms", methods=["POST"])
def sms_webhook():
    """Handle incoming SMS messages from patients"""
    try:
        # Get message details from Twilio
        from_number = request.form.get("From")
        message_body = request.form.get("Body", "")
        message_sid = request.form.get("MessageSid")

        print(f"📱 Incoming SMS from {from_number}: {message_body}")

        # Check if this is a reschedule selection (number 1-5)
        if message_body.strip().isdigit():
            response_text = sms_service.handle_reschedule_selection(
                from_number, message_body
            )
        else:
            # Process normal patient response
            response_text = sms_service.process_patient_response(
                from_number, message_body
            )

        print(f"🤖 Sending response: {response_text[:100]}...")

        # Create TwiML response
        twiml_response = sms_service.create_twiml_response(response_text)

        return twiml_response, 200, {"Content-Type": "text/xml"}

    except Exception as e:
        print(f"❌ Error processing SMS webhook: {e}")
        error_response = sms_service.create_twiml_response(
            "Sorry, we're experiencing technical difficulties. Please call our office."
        )
        return error_response, 500, {"Content-Type": "text/xml"}


@app.route("/webhook/test", methods=["GET", "POST"])
def test_webhook():
    """Test endpoint to verify webhook is working"""
    if request.method == "GET":
        return {
            "status": "ok",
            "message": "Dentist Office SMS System is running!",
            "timestamp": datetime.now().isoformat(),
            "endpoints": [
                "POST /webhook/sms - SMS webhook",
                "GET /webhook/test - This test endpoint",
                "POST /send-reminders - Manual reminder trigger",
                "GET /appointments - View appointments",
            ],
        }
    else:
        # Test SMS processing with sample data
        test_phone = "+1234567890"
        test_message = "CONFIRM"

        response = sms_service.process_patient_response(test_phone, test_message)

        return {
            "status": "test_completed",
            "test_phone": test_phone,
            "test_message": test_message,
            "response": response,
        }


@app.route("/send-reminders", methods=["POST", "GET"])
def send_reminders():
    """Manually trigger sending appointment reminders"""
    try:
        sent_count = sms_service.send_bulk_reminders()

        return {
            "status": "success",
            "message": f"Sent {sent_count} appointment reminders",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send reminders: {str(e)}",
        }, 500


@app.route("/appointments")
def view_appointments():
    """View all appointments in JSON format"""
    appointments = appointment_manager.get_all_appointments()

    appointments_data = []
    for apt in appointments:
        appointments_data.append(
            {
                "id": apt.appointment_id,
                "patient_name": apt.patient_name,
                "patient_phone": apt.patient_phone,
                "date": apt.appointment_date,
                "time": apt.appointment_time,
                "service": apt.service,
                "status": apt.status,
                "reminder_sent": apt.reminder_sent,
                "formatted_info": apt.format_appointment_info(),
            }
        )

    return {
        "total_appointments": len(appointments_data),
        "appointments": appointments_data,
        "timestamp": datetime.now().isoformat(),
    }


@app.route("/add-appointment", methods=["POST"])
def add_appointment():
    """Add a new appointment via API"""
    try:
        data = request.get_json()

        appointment = Appointment(
            appointment_id=data["appointment_id"],
            patient_name=data["patient_name"],
            patient_phone=data["patient_phone"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            service=data.get("service", "General Checkup"),
        )

        success = appointment_manager.add_appointment(appointment)

        if success:
            return {
                "status": "success",
                "message": "Appointment added successfully",
                "appointment_id": appointment.appointment_id,
            }
        else:
            return {"status": "error", "message": "Appointment ID already exists"}, 400

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to add appointment: {str(e)}",
        }, 500


def schedule_daily_reminders():
    """Schedule daily reminder sending"""
    schedule.every().day.at("09:00").do(sms_service.send_bulk_reminders)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def start_scheduler():
    """Start the background scheduler for daily reminders"""
    scheduler_thread = threading.Thread(target=schedule_daily_reminders, daemon=True)
    scheduler_thread.start()
    print("📅 Daily reminder scheduler started (9:00 AM)")


if __name__ == "__main__":
    print("🚀 Starting Dentist Office SMS Appointment System...")

    # Create sample appointments if none exist
    if not appointment_manager.get_all_appointments():
        print("📝 Creating sample appointments...")
        create_sample_appointments()

    # Start the scheduler for daily reminders
    start_scheduler()

    # Get configuration
    port = int(os.getenv("FLASK_PORT", 5000))
    office_name = os.getenv("OFFICE_NAME", "Dental Office")

    print(f"\n🦷 {office_name} SMS System")
    print("=" * 50)
    print(f"📍 Server running on: http://localhost:{port}")
    print(f"📱 SMS webhook endpoint: /webhook/sms")
    print(f"🧪 Test endpoint: /webhook/test")
    print("\n💡 To expose to internet:")
    print(f"   ngrok http {port}")
    print("\n📋 Dashboard: http://localhost:{port}")

    # Run the Flask app
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
