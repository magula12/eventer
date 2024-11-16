import unittest
from datetime import datetime
from ..event import Event
from ..eventCategory import EventCategory
from ..person import Person
from ..role import Role

class TestEvent(unittest.TestCase):
    def setUp(self):
        category = EventCategory(id=1, techName="Conference", description="Conferences", priority=1)
        self.event = Event(id=1, category=category, priority=1, name="Tech Conf",
                           start_date=datetime(2024, 10, 10,9),
                           description="Tech conference 2024")

    def test_event_creation(self):
        self.assertEqual(self.event.name, "Tech Conf")
        self.assertEqual(self.event.get_category().techName, "Conference")
        self.assertEqual(self.event.priority, 1)
        self.assertEqual(self.event.description, "Tech conference 2024")

    def test_event_add_remove_participant(self):
        participant = Person(id=2, name="Alice", surname="Smith", admin=False, email="alice@example.com", phone_number="987654321")
        self.event.add_participant(participant, Role(id=1, name="Attendee",priority=3))
        self.assertIn(participant, self.event.get_participants())
        self.event.remove_participant(participant)
        self.assertNotIn(participant, self.event.get_participants())
