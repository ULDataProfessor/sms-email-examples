#!/usr/bin/env python3
"""
Test script for the Dentist Office SMS Appointment System
This script demonstrates the system functionality without sending actual SMS messages.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from appointment_manager import (
    appointment_manager,
    Appointment,
    create_sample_appointments,
)
from sms_service import SMSService


class MockSMSService(SMSService):
    """Mock SMS service for testing without actually sending SMS"""

    def __init__(self):
        # Set up mock environment variables if they don't exist
        os.environ.setdefault("TWILIO_ACCOUNT_SID", "test_sid")
        os.environ.setdefault("TWILIO_AUTH_TOKEN", "test_token")
        os.environ.setdefault("TWILIO_PHONE_NUMBER", "+1234567890")
        os.environ.setdefault("OFFICE_NAME", "Test Dental Office")
        os.environ.setdefault("OFFICE_PHONE", "+1234567890")

        # Initialize without actual Twilio client
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.office_name = os.getenv("OFFICE_NAME", "Dental Office")
        self.office_phone = os.getenv("OFFICE_PHONE")

    def send_appointment_reminder(self, appointment):
        """Mock sending appointment reminder"""
        reminder_message = self._create_reminder_message(appointment)
        print(f"📱 MOCK SMS to {appointment.patient_phone}:")
        print(f"Message: {reminder_message}")
        print("-" * 60)

        appointment_manager.mark_reminder_sent(appointment.appointment_id)
        return True


def test_appointment_management():
    """Test appointment management functionality"""
    print("🧪 Testing Appointment Management")
    print("=" * 50)

    # Clear existing appointments for clean test
    appointment_manager.appointments = {}

    # Create test appointments
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    test_appointments = [
        Appointment(
            appointment_id="TEST001",
            patient_name="John Doe",
            patient_phone="+1555123456",
            appointment_date=tomorrow,
            appointment_time="10:00",
            service="Teeth Cleaning",
        ),
        Appointment(
            appointment_id="TEST002",
            patient_name="Jane Smith",
            patient_phone="+1555987654",
            appointment_date=tomorrow,
            appointment_time="14:00",
            service="Root Canal",
        ),
        Appointment(
            appointment_id="TEST003",
            patient_name="Bob Johnson",
            patient_phone="+1555555555",
            appointment_date=next_week,
            appointment_time="09:00",
            service="Consultation",
        ),
    ]

    # Add appointments
    for apt in test_appointments:
        success = appointment_manager.add_appointment(apt)
        print(f"✅ Added appointment: {apt.patient_name} - {success}")

    # Test retrieval
    all_appointments = appointment_manager.get_all_appointments()
    print(f"\n📅 Total appointments: {len(all_appointments)}")

    tomorrow_appointments = appointment_manager.get_tomorrows_appointments()
    print(f"📅 Tomorrow's appointments: {len(tomorrow_appointments)}")

    return test_appointments


def test_sms_processing():
    """Test SMS response processing"""
    print("\n🧪 Testing SMS Response Processing")
    print("=" * 50)

    mock_sms = MockSMSService()
    test_phone = "+1555123456"

    # Test different patient responses
    test_responses = [
        ("CONFIRM", "Appointment confirmation"),
        ("RESCHEDULE", "Reschedule request"),
        ("CANCEL", "Appointment cancellation"),
        ("1", "Reschedule slot selection"),
        ("HELLO", "Unknown command (help response)"),
    ]

    for response_text, description in test_responses:
        print(f"\n🔄 Testing: {description}")
        print(f"Patient response: '{response_text}'")

        response = mock_sms.process_patient_response(test_phone, response_text)
        print(f"System response: {response[:100]}...")

        if len(response) > 100:
            print("...")


def test_reminder_sending():
    """Test appointment reminder sending"""
    print("\n🧪 Testing Appointment Reminder Sending")
    print("=" * 50)

    mock_sms = MockSMSService()
    tomorrow_appointments = appointment_manager.get_tomorrows_appointments()

    if tomorrow_appointments:
        for appointment in tomorrow_appointments:
            print(f"\n📨 Sending reminder to {appointment.patient_name}")
            mock_sms.send_appointment_reminder(appointment)
    else:
        print("No appointments scheduled for tomorrow.")


def test_reschedule_flow():
    """Test the complete reschedule flow"""
    print("\n🧪 Testing Complete Reschedule Flow")
    print("=" * 50)

    mock_sms = MockSMSService()
    test_phone = "+1555123456"

    # Step 1: Patient requests reschedule
    print("👤 Patient: RESCHEDULE")
    response1 = mock_sms.process_patient_response(test_phone, "RESCHEDULE")
    print(f"🤖 System: {response1[:200]}...")

    # Step 2: Patient selects option
    print("\n👤 Patient: 2")
    response2 = mock_sms.handle_reschedule_selection(test_phone, "2")
    print(f"🤖 System: {response2}")


def test_appointment_statuses():
    """Test appointment status updates"""
    print("\n🧪 Testing Appointment Status Updates")
    print("=" * 50)

    appointments = appointment_manager.get_all_appointments()
    if appointments:
        test_appointment = appointments[0]
        original_status = test_appointment.status

        # Test status updates
        statuses = ["confirmed", "cancelled", "completed"]
        for status in statuses:
            success = appointment_manager.update_appointment_status(
                test_appointment.appointment_id, status
            )
            print(
                f"✅ Updated {test_appointment.patient_name} status to '{status}': {success}"
            )

        # Reset to original status
        appointment_manager.update_appointment_status(
            test_appointment.appointment_id, original_status
        )


def display_system_overview():
    """Display system overview"""
    print("\n📊 System Overview")
    print("=" * 50)

    appointments = appointment_manager.get_all_appointments()
    statuses = {}

    for apt in appointments:
        statuses[apt.status] = statuses.get(apt.status, 0) + 1

    print(f"Total appointments: {len(appointments)}")
    for status, count in statuses.items():
        print(f"  {status.title()}: {count}")

    tomorrow_count = len(appointment_manager.get_tomorrows_appointments())
    print(f"Tomorrow's appointments: {tomorrow_count}")


def main():
    """Main test function"""
    print("🦷 Dentist Office SMS System - Test Suite")
    print("=" * 60)
    print(
        "This script tests the system functionality without sending actual SMS messages.\n"
    )

    try:
        # Run all tests
        test_appointment_management()
        test_sms_processing()
        test_reminder_sending()
        test_reschedule_flow()
        test_appointment_statuses()
        display_system_overview()

        print("\n✅ All tests completed successfully!")
        print("\n💡 To run the actual system:")
        print("1. Configure your .env file with real Twilio credentials")
        print("2. Run: python app.py")
        print("3. Start ngrok: ngrok http 5000")
        print("4. Configure Twilio webhook URL")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
