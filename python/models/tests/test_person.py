import unittest

from ..person import Person
from ..role import Role

from datetime import datetime

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person(id=1, name="John", surname="Doe",
                             admin=True, email="john@example.com", phone_number="123456789")
        self.person.add_off_time(datetime(2024, 11, 14, 10, 0), datetime(2024, 11, 14, 12, 0))
        self.person.add_off_time(datetime(2024, 11, 14, 14, 0), datetime(2024, 11, 14, 15, 0))

    def test_person_creation(self):
        self.assertEqual(self.person.name, "John")
        self.assertEqual(self.person.surname, "Doe")
        self.assertEqual(self.person.admin, True)
        self.assertEqual(self.person.email, "john@example.com")
        self.assertEqual(self.person.phone_number, "123456789")

    def test_person_add_role(self):
        role = Role(id=1, name="Sound Engineer", priority=2)
        self.person.add_role(role, rating=4)
        self.assertEqual(len(self.person.roles), 1)
        self.assertEqual(self.person.roles[0]['role'].name, "Sound Engineer")
        self.assertEqual(self.person.roles[0]['rating'], 4)

    def test_person_get_full_name(self):
        self.assertEqual(self.person.get_full_name(), "John Doe")

    def test_person_setters_getters(self):
        self.person.set_name("Jane")
        self.person.set_surname("Smith")
        self.person.set_email("jane@example.com")
        self.person.set_phone_number("987654321")
        self.assertEqual(self.person.get_name(), "Jane")
        self.assertEqual(self.person.get_surname(), "Smith")
        self.assertEqual(self.person.get_email(), "jane@example.com")
        self.assertEqual(self.person.get_phone_number(), "987654321")

    def test_person_is_admin(self):
        self.assertTrue(self.person.is_admin())
        self.person.set_admin(False)
        self.assertFalse(self.person.is_admin())

    def test_is_free_when_no_overlap(self):
        """Test is_free method when there is no overlap with off-times."""
        start_date = datetime(2024, 11, 14, 12, 30)
        end_date = datetime(2024, 11, 14, 13, 30)
        self.assertTrue(self.person.is_free(start_date, end_date), "The person should be free during this time.")

    def test_is_free_when_exact_overlap(self):
        """Test is_free method when the requested period exactly matches an off-time."""
        start_date = datetime(2024, 11, 14, 10, 0)
        end_date = datetime(2024, 11, 14, 12, 0)
        self.assertFalse(self.person.is_free(start_date, end_date),
                         "The person should not be free during this exact off-time.")

    def test_is_free_when_partial_overlap(self):
        """Test is_free method when the requested period partially overlaps an off-time."""
        start_date = datetime(2024, 11, 14, 11, 0)
        end_date = datetime(2024, 11, 14, 13, 0)
        self.assertFalse(self.person.is_free(start_date, end_date),
                         "The person should not be free due to partial overlap.")

    def test_is_free_when_fully_within_off_time(self):
        """Test is_free method when the requested period is fully within an off-time."""
        start_date = datetime(2024, 11, 14, 10, 30)
        end_date = datetime(2024, 11, 14, 11, 30)
        self.assertFalse(self.person.is_free(start_date, end_date),
                         "The person should not be free when fully within an off-time.")

    def test_is_free_when_before_off_time(self):
        """Test is_free method when the requested period is before any off-time."""
        start_date = datetime(2024, 11, 14, 8, 0)
        end_date = datetime(2024, 11, 14, 9, 0)
        self.assertTrue(self.person.is_free(start_date, end_date),
                        "The person should be free before the first off-time.")

    def test_is_free_when_after_off_time(self):
        """Test is_free method when the requested period is after any off-time."""
        start_date = datetime(2024, 11, 14, 15, 30)
        end_date = datetime(2024, 11, 14, 16, 30)
        self.assertTrue(self.person.is_free(start_date, end_date), "The person should be free after the last off-time.")

    def test_is_free_with_overlap_multiple_off_times(self):
        """Test is_free method when overlapping multiple off-time periods."""
        start_date = datetime(2024, 11, 14, 11, 30)
        end_date = datetime(2024, 11, 14, 14, 30)
        self.assertFalse(self.person.is_free(start_date, end_date),
                         "The person should not be free due to overlap with multiple off-times.")