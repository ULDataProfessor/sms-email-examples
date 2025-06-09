"""
Appointment Management System for Dentist Office
Handles appointment storage, retrieval, and modifications.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class Appointment:
    """Represents a single appointment"""

    def __init__(
        self,
        appointment_id: str,
        patient_name: str,
        patient_phone: str,
        appointment_date: str,
        appointment_time: str,
        service: str = "General Checkup",
        status: str = "scheduled",
    ):
        self.appointment_id = appointment_id
        self.patient_name = patient_name
        self.patient_phone = patient_phone
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.service = service
        self.status = status  # scheduled, confirmed, cancelled, completed
        self.reminder_sent = False
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert appointment to dictionary"""
        return {
            "appointment_id": self.appointment_id,
            "patient_name": self.patient_name,
            "patient_phone": self.patient_phone,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
            "service": self.service,
            "status": self.status,
            "reminder_sent": self.reminder_sent,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Appointment":
        """Create appointment from dictionary"""
        appointment = cls(
            appointment_id=data["appointment_id"],
            patient_name=data["patient_name"],
            patient_phone=data["patient_phone"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            service=data.get("service", "General Checkup"),
            status=data.get("status", "scheduled"),
        )
        appointment.reminder_sent = data.get("reminder_sent", False)
        appointment.created_at = data.get("created_at", datetime.now().isoformat())
        return appointment

    def get_datetime(self) -> datetime:
        """Get appointment as datetime object"""
        datetime_str = f"{self.appointment_date} {self.appointment_time}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    def is_tomorrow(self) -> bool:
        """Check if appointment is tomorrow"""
        appointment_dt = self.get_datetime()
        tomorrow = datetime.now().date() + timedelta(days=1)
        return appointment_dt.date() == tomorrow

    def format_appointment_info(self) -> str:
        """Format appointment info for SMS"""
        date_obj = datetime.strptime(self.appointment_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%A, %B %d, %Y")

        time_obj = datetime.strptime(self.appointment_time, "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")

        return f"{formatted_date} at {formatted_time}"


class AppointmentManager:
    """Manages all appointments for the dentist office"""

    def __init__(self, data_file: str = "appointments.json"):
        self.data_file = data_file
        self.appointments: Dict[str, Appointment] = {}
        self.load_appointments()

    def load_appointments(self):
        """Load appointments from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    for apt_id, apt_data in data.items():
                        self.appointments[apt_id] = Appointment.from_dict(apt_data)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading appointments: {e}")
                self.appointments = {}

    def save_appointments(self):
        """Save appointments to file"""
        data = {}
        for apt_id, appointment in self.appointments.items():
            data[apt_id] = appointment.to_dict()

        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_appointment(self, appointment: Appointment) -> bool:
        """Add a new appointment"""
        if appointment.appointment_id in self.appointments:
            return False

        self.appointments[appointment.appointment_id] = appointment
        self.save_appointments()
        return True

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get appointment by ID"""
        return self.appointments.get(appointment_id)

    def get_appointment_by_phone(self, phone: str) -> Optional[Appointment]:
        """Get the most recent appointment for a phone number"""
        phone_appointments = [
            apt
            for apt in self.appointments.values()
            if apt.patient_phone == phone and apt.status != "cancelled"
        ]

        if not phone_appointments:
            return None

        # Return the most recent scheduled appointment
        phone_appointments.sort(key=lambda x: x.get_datetime())
        return phone_appointments[0]

    def update_appointment_status(self, appointment_id: str, status: str) -> bool:
        """Update appointment status"""
        if appointment_id not in self.appointments:
            return False

        self.appointments[appointment_id].status = status
        self.save_appointments()
        return True

    def reschedule_appointment(
        self, appointment_id: str, new_date: str, new_time: str
    ) -> bool:
        """Reschedule an appointment"""
        if appointment_id not in self.appointments:
            return False

        appointment = self.appointments[appointment_id]
        appointment.appointment_date = new_date
        appointment.appointment_time = new_time
        appointment.status = "scheduled"
        appointment.reminder_sent = False
        self.save_appointments()
        return True

    def get_tomorrows_appointments(self) -> List[Appointment]:
        """Get all appointments for tomorrow that need reminders"""
        tomorrow_appointments = []
        for appointment in self.appointments.values():
            if (
                appointment.is_tomorrow()
                and not appointment.reminder_sent
                and appointment.status == "scheduled"
            ):
                tomorrow_appointments.append(appointment)

        return tomorrow_appointments

    def mark_reminder_sent(self, appointment_id: str):
        """Mark that reminder has been sent for an appointment"""
        if appointment_id in self.appointments:
            self.appointments[appointment_id].reminder_sent = True
            self.save_appointments()

    def get_all_appointments(self) -> List[Appointment]:
        """Get all appointments"""
        return list(self.appointments.values())

    def get_available_slots(self, date: str) -> List[str]:
        """Get available time slots for a given date"""
        # Standard office hours: 9 AM to 5 PM, 1-hour slots
        all_slots = [
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
        ]

        # Get booked slots for the date
        booked_slots = [
            apt.appointment_time
            for apt in self.appointments.values()
            if apt.appointment_date == date and apt.status != "cancelled"
        ]

        # Return available slots
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        return available_slots


# Initialize the appointment manager
appointment_manager = AppointmentManager()


def create_sample_appointments():
    """Create some sample appointments for testing"""
    from datetime import datetime, timedelta

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    sample_appointments = [
        Appointment(
            appointment_id="APT001",
            patient_name="John Smith",
            patient_phone="+1234567890",
            appointment_date=tomorrow,
            appointment_time="10:00",
            service="Cleaning",
        ),
        Appointment(
            appointment_id="APT002",
            patient_name="Jane Doe",
            patient_phone="+1987654321",
            appointment_date=tomorrow,
            appointment_time="14:00",
            service="Root Canal",
        ),
        Appointment(
            appointment_id="APT003",
            patient_name="Bob Johnson",
            patient_phone="+1555666777",
            appointment_date=next_week,
            appointment_time="09:00",
            service="Consultation",
        ),
    ]

    for appointment in sample_appointments:
        appointment_manager.add_appointment(appointment)

    print("✅ Sample appointments created!")


if __name__ == "__main__":
    # Create sample appointments for testing
    create_sample_appointments()

    # Display all appointments
    appointments = appointment_manager.get_all_appointments()
    print(f"\n📅 Total appointments: {len(appointments)}")

    for apt in appointments:
        print(f"- {apt.patient_name}: {apt.format_appointment_info()} ({apt.status})")
