"""
SMS Service for Dentist Office Appointment System
Handles sending appointment reminders and processing patient responses via Twilio.
"""

import os
import re
from datetime import datetime, timedelta
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from appointment_manager import appointment_manager, Appointment

load_dotenv()


class SMSService:
    """Handles SMS operations using Twilio"""

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.office_name = os.getenv("OFFICE_NAME", "Dental Office")
        self.office_phone = os.getenv("OFFICE_PHONE")

        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError(
                "Missing required Twilio credentials in environment variables"
            )

        self.client = Client(self.account_sid, self.auth_token)

    def send_appointment_reminder(self, appointment: Appointment) -> bool:
        """Send appointment reminder SMS"""
        try:
            reminder_message = self._create_reminder_message(appointment)

            message = self.client.messages.create(
                body=reminder_message,
                from_=self.from_number,
                to=appointment.patient_phone,
            )

            print(f"✅ Reminder sent to {appointment.patient_name}: {message.sid}")
            appointment_manager.mark_reminder_sent(appointment.appointment_id)
            return True

        except Exception as e:
            print(f"❌ Failed to send reminder to {appointment.patient_name}: {e}")
            return False

    def _create_reminder_message(self, appointment: Appointment) -> str:
        """Create appointment reminder message"""
        appointment_info = appointment.format_appointment_info()

        message = f"🦷 {self.office_name} Reminder\n\n"
        message += f"Hi {appointment.patient_name}!\n\n"
        message += f"You have an appointment for {appointment.service} "
        message += f"tomorrow ({appointment_info}).\n\n"
        message += "Please reply:\n"
        message += "• CONFIRM to confirm your appointment\n"
        message += "• RESCHEDULE to change the date/time\n"
        message += "• CANCEL to cancel your appointment\n\n"

        if self.office_phone:
            message += f"Questions? Call us at {self.office_phone}"

        return message

    def process_patient_response(self, from_number: str, message_body: str) -> str:
        """Process incoming SMS response from patient"""
        # Clean and normalize the message
        message_body = message_body.strip().upper()

        # Find the patient's appointment
        appointment = appointment_manager.get_appointment_by_phone(from_number)

        if not appointment:
            return self._create_no_appointment_response()

        # Process different response types
        if "CONFIRM" in message_body or "YES" in message_body:
            return self._handle_confirmation(appointment)

        elif "RESCHEDULE" in message_body or "CHANGE" in message_body:
            return self._handle_reschedule_request(appointment)

        elif "CANCEL" in message_body or "NO" in message_body:
            return self._handle_cancellation(appointment)

        else:
            return self._create_help_response(appointment)

    def _handle_confirmation(self, appointment: Appointment) -> str:
        """Handle appointment confirmation"""
        appointment_manager.update_appointment_status(
            appointment.appointment_id, "confirmed"
        )

        response = f"✅ Thank you, {appointment.patient_name}! "
        response += f"Your appointment for {appointment.service} on "
        response += f"{appointment.format_appointment_info()} is CONFIRMED.\n\n"
        response += f"See you then! - {self.office_name}"

        return response

    def _handle_cancellation(self, appointment: Appointment) -> str:
        """Handle appointment cancellation"""
        appointment_manager.update_appointment_status(
            appointment.appointment_id, "cancelled"
        )

        response = f"❌ Your appointment for {appointment.service} on "
        response += f"{appointment.format_appointment_info()} has been CANCELLED.\n\n"
        response += "We're sorry to see you go. If you'd like to reschedule, "

        if self.office_phone:
            response += f"please call us at {self.office_phone}.\n\n"
        else:
            response += "please contact our office.\n\n"

        response += f"- {self.office_name}"

        return response

    def _handle_reschedule_request(self, appointment: Appointment) -> str:
        """Handle reschedule request"""
        # Get available slots for next few days
        available_slots = self._get_next_available_slots()

        response = f"📅 Reschedule Request Received\n\n"
        response += f"Current appointment: {appointment.service} on "
        response += f"{appointment.format_appointment_info()}\n\n"
        response += "Available slots:\n"

        for i, slot in enumerate(available_slots[:5], 1):  # Show first 5 slots
            date_str = slot["date"]
            time_str = slot["time"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %m/%d")
            time_obj = datetime.strptime(time_str, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")

            response += f"{i}. {formatted_date} at {formatted_time}\n"

        response += f"\nReply with the number (1-{min(5, len(available_slots))}) "
        response += "of your preferred slot, or call us for more options.\n\n"

        if self.office_phone:
            response += f"Call: {self.office_phone}"

        return response

    def _get_next_available_slots(self) -> list:
        """Get next available appointment slots"""
        available_slots = []
        current_date = datetime.now().date() + timedelta(days=1)

        # Check next 14 days
        for i in range(14):
            check_date = current_date + timedelta(days=i)
            date_str = check_date.strftime("%Y-%m-%d")

            # Skip weekends (assuming office is closed)
            if check_date.weekday() >= 5:
                continue

            slots = appointment_manager.get_available_slots(date_str)
            for slot_time in slots:
                available_slots.append({"date": date_str, "time": slot_time})

        return available_slots

    def _create_no_appointment_response(self) -> str:
        """Create response when no appointment is found"""
        response = f"❓ We couldn't find an upcoming appointment for this number.\n\n"

        if self.office_phone:
            response += f"Please call us at {self.office_phone} for assistance.\n\n"

        response += f"- {self.office_name}"

        return response

    def _create_help_response(self, appointment: Appointment) -> str:
        """Create help response with available commands"""
        response = f"🤔 I didn't understand that. Here are your options:\n\n"
        response += f"Your appointment: {appointment.service} on "
        response += f"{appointment.format_appointment_info()}\n\n"
        response += "Reply with:\n"
        response += "• CONFIRM - to confirm your appointment\n"
        response += "• RESCHEDULE - to change the date/time\n"
        response += "• CANCEL - to cancel your appointment\n\n"

        if self.office_phone:
            response += f"Or call us at {self.office_phone}"

        return response

    def handle_reschedule_selection(self, from_number: str, selection: str) -> str:
        """Handle when patient selects a reschedule option"""
        try:
            slot_number = int(selection.strip())
            if slot_number < 1 or slot_number > 5:
                return "❌ Please choose a number between 1-5, or call our office."

            appointment = appointment_manager.get_appointment_by_phone(from_number)
            if not appointment:
                return self._create_no_appointment_response()

            available_slots = self._get_next_available_slots()
            if slot_number > len(available_slots):
                return "❌ That slot is no longer available. Please call our office."

            selected_slot = available_slots[slot_number - 1]
            new_date = selected_slot["date"]
            new_time = selected_slot["time"]

            # Update the appointment
            success = appointment_manager.reschedule_appointment(
                appointment.appointment_id, new_date, new_time
            )

            if success:
                updated_appointment = appointment_manager.get_appointment(
                    appointment.appointment_id
                )
                response = f"✅ Appointment rescheduled!\n\n"
                response += f"New appointment: {updated_appointment.service} on "
                response += f"{updated_appointment.format_appointment_info()}\n\n"
                response += f"Thank you! - {self.office_name}"
                return response
            else:
                return (
                    "❌ Sorry, there was an error rescheduling. Please call our office."
                )

        except ValueError:
            return "❌ Please reply with a number (1-5) or call our office."

    def send_bulk_reminders(self) -> int:
        """Send reminders to all patients with appointments tomorrow"""
        tomorrow_appointments = appointment_manager.get_tomorrows_appointments()

        sent_count = 0
        for appointment in tomorrow_appointments:
            if self.send_appointment_reminder(appointment):
                sent_count += 1

        print(f"📱 Sent {sent_count} appointment reminders")
        return sent_count

    def create_twiml_response(self, message: str) -> str:
        """Create TwiML response for webhook"""
        response = MessagingResponse()
        response.message(message)
        return str(response)


# Initialize SMS service
sms_service = SMSService()


def test_sms_service():
    """Test the SMS service functionality"""
    print("🧪 Testing SMS Service...")

    # Test reminder message creation
    from appointment_manager import create_sample_appointments

    create_sample_appointments()

    appointments = appointment_manager.get_all_appointments()
    if appointments:
        test_appointment = appointments[0]
        reminder_msg = sms_service._create_reminder_message(test_appointment)
        print(f"\n📱 Sample reminder message:\n{reminder_msg}\n")

    # Test response processing
    test_responses = [
        ("CONFIRM", "Confirmation test"),
        ("RESCHEDULE", "Reschedule test"),
        ("CANCEL", "Cancellation test"),
        ("HELLO", "Help response test"),
    ]

    for response_text, description in test_responses:
        print(f"🔄 {description}:")
        response = sms_service.process_patient_response("+1234567890", response_text)
        print(f"Response: {response[:100]}...\n")


if __name__ == "__main__":
    test_sms_service()
