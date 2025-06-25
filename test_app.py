import unittest
import datetime
import os
from unittest.mock import patch

from dotenv import load_dotenv
load_dotenv()

from daily_assigner import (
    get_assigned_person_for_today,
    DAILY_ASSIGNMENTS,
    PHONE_DIRECTORY,
    DEFAULT_CONTACT,
    EDWARD, JOHNNY_R, CHRIS, JOHNNATHAN
)
from incoming_call_router import app as flask_app

class TestCallRouterApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Verify environment variables and configuration."""
        # Check all required environment variables
        required_names = [EDWARD, JOHNNY_R, CHRIS, JOHNNATHAN, DEFAULT_CONTACT]
        for name in required_names:
            if os.getenv(name) is None:
                raise ValueError(f"Missing environment variable: {name}")
            if name not in PHONE_DIRECTORY or PHONE_DIRECTORY[name] is None:
                raise ValueError(f"Missing or invalid phone number for {name}")

        # Verify all assignments have valid phone numbers
        for day, person in DAILY_ASSIGNMENTS.items():
            if person not in PHONE_DIRECTORY or PHONE_DIRECTORY[person] is None:
                raise ValueError(f"Invalid assignment for day {day}: {person}")
        
        # Store default phone number
        cls.default_phone = PHONE_DIRECTORY[DEFAULT_CONTACT]

    def setUp(self):
        """Set up Flask test client."""
        self.app_context = flask_app.app_context()
        self.app_context.push()
        flask_app.testing = True
        self.client = flask_app.test_client()

    def tearDown(self):
        """Clean up after test."""
        self.app_context.pop()

    def _get_expected_assignment(self, day_index):
        """Get expected name and phone for a given day."""
        name = DAILY_ASSIGNMENTS.get(day_index, self.default_phone)
        phone = PHONE_DIRECTORY.get(name, self.default_phone)
        return name, phone

    def test_get_assigned_person_for_today_current_day(self):
        """Test assignment for current day."""
        now = datetime.datetime.now()
        day_idx = now.weekday()
        expected_day_name = now.strftime("%A")

        with patch('daily_assigner.datetime.datetime') as mock_dt:
            mock_dt.now.return_value = now
            name, phone, day_name = get_assigned_person_for_today()

        expected_name, expected_phone = self._get_expected_assignment(day_idx)
        self.assertEqual(name, expected_name)
        self.assertEqual(phone, expected_phone)
        self.assertEqual(day_name, expected_day_name)
        self.assertIsNotNone(phone)

    def test_get_assigned_person_for_each_day_of_week(self):
        """Test assignments for each day of the week."""
        test_date = datetime.datetime(2023, 10, 26)  # Thursday
        expected_day_name = test_date.strftime("%A")
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        with patch('daily_assigner.datetime.datetime') as mock_dt:
            mock_dt.now.return_value = test_date

            for day_idx in range(7):
                name, phone, day_name = get_assigned_person_for_today(test_todays_day=day_idx)
                expected_name, expected_phone = self._get_expected_assignment(day_idx)
                
                msg = f"For {day_names[day_idx]} (index {day_idx})"
                self.assertEqual(name, expected_name, f"{msg}: Name mismatch")
                self.assertEqual(phone, expected_phone, f"{msg}: Phone mismatch")
                self.assertEqual(day_name, expected_day_name, f"{msg}: Day name mismatch")
                self.assertIsNotNone(phone, f"{msg}: Phone is None")

    def test_voice_webhook_api(self):
        """Test the /voice API endpoint."""
        # Get the current day's assignment without mocking
        # This tests the actual implementation as requested
        current_day = datetime.datetime.now().weekday()
        _, expected_phone, _ = get_assigned_person_for_today(test_todays_day=current_day)

        response = self.client.post("/voice")

        self.assertEqual(response.status_code, 200)
        # Flask returns text/html by default, not application/xml
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

        response_xml = response.data.decode('utf-8')
        self.assertIn("<Response>", response_xml)
        self.assertIn("<Dial>", response_xml)
        self.assertIn(f"<Number>{expected_phone}</Number>", response_xml)

if __name__ == '__main__':
    unittest.main()
