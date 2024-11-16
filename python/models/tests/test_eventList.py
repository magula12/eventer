from unittest import TestCase
from datetime import datetime

from ..event import Event
from ..eventCategory import EventCategory
from ..eventList import EventList
from ..role import Role

class TestEventList(TestCase):

    def setUp(self):
        self.event1 = Event(1, EventCategory(123,"Meeting","fakt huste",3),
                            1, "Event 1", datetime(2023, 10, 1,10), "Description 1")
        self.event2 = Event(2, EventCategory(13,"Workshop", "nuda",4),
                            2, "Event 2", datetime(2023, 10, 2,11),"Description 2")
        self.event_list = EventList([self.event1, self.event2])

    def test_add_event(self):
        event3 = Event(3, EventCategory(12,"Conference",'daka konfera', 7),
                       3, "Event 3", datetime(2023, 10, 3,12),"Description 3")
        self.event_list.add_event(event3)
        self.assertIn(event3, self.event_list.get_events())

    def test_remove_event_by_index(self):
        self.event_list.remove_event(0)
        self.assertNotIn(self.event1, self.event_list.get_events())

    def test_remove_event_by_object(self):
        self.event_list.remove_event(self.event1)
        self.assertNotIn(self.event1, self.event_list.get_events())

    def test_remove_event_invalid_index(self):
        with self.assertRaises(IndexError):
            self.event_list.remove_event(10)

    def test_remove_event_not_in_list(self):
        event3 = Event(3, EventCategory(12,"Conference",'daka konfera', 7),
                       3, "Event 3", datetime(2023, 10, 3,12),"Description 3")
        with self.assertRaises(ValueError):
            self.event_list.remove_event(event3)

    def test_get_event(self):
        self.assertEqual(self.event_list.get_event(0), self.event1)
        self.assertEqual(self.event_list.get_event(1), self.event2)

    def test_get_events(self):
        self.assertEqual(self.event_list.get_events(), [self.event1, self.event2])
