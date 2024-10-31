import unittest
from datetime import date, time
from ..event import Event
from ..eventCategory import EventCategory
from ..person import Person

class TestEvent(unittest.TestCase):
    def setUp(self):
        category = EventCategory(id=1, techName="Conference", description="Conferences", priority=1)
        self.event = Event(id=1, category=category, priority=1, name="Tech Conf", date=date(2024, 10, 10), time=time(9, 0), description="Tech conference 2024")

    def test_event_creation(self):
        self.assertEqual(self.event.name, "Tech Conf")
        self.assertEqual(self.event.get_category().techName, "Conference")
        self.assertEqual(self.event.priority, 1)
        self.assertEqual(self.event.description, "Tech conference 2024")

    def test_event_add_remove_participant(self):
        participant = Person(id=2, name="Alice", surname="Smith", admin=False, email="alice@example.com", phone_number="987654321")
        self.event.add_participant(participant)
        self.assertIn(participant, self.event.get_participants())
        self.event.remove_participant(participant)
        self.assertNotIn(participant, self.event.get_participants())

    def test_event_is_happening_today(self):
        self.event.date = date.today()
        self.assertTrue(self.event.is_happening_today())
