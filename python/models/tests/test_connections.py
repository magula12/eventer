import unittest
from datetime import date, time

from ..connections import EventPerson, PersonRoleQualification
from ..person import Person
from ..event import Event
from ..eventCategory import EventCategory
from ..role import Role

class TestEventPerson(unittest.TestCase):
    def setUp(self):
        self.event = Event(id=1, category=EventCategory(id=1, techName="Workshop", description="Workshop events", priority=2), priority=1, name="Workshop 101", date=date(2024, 12, 12), time=time(10, 0), description="Basic workshop")
        self.person = Person(id=3, name="Bob", surname="Brown", admin=False, email="bob@example.com", phone_number="123456789")
        self.event_person = EventPerson(event=self.event, person=self.person)

    def test_event_person_link(self):
        self.assertEqual(self.event_person.event.name, "Workshop 101")
        self.assertEqual(self.event_person.person.get_full_name(), "Bob Brown")

    def test_event_person_event_person_relationship(self):
        self.assertEqual(self.event_person.event, self.event)
        self.assertEqual(self.event_person.person, self.person)

class TestPersonRoleQualification(unittest.TestCase):
    def setUp(self):
        category = EventCategory(id=1, techName="Seminar", description="Seminar events", priority=3)
        role = Role(id=1, name="Speaker", priority=1)
        person = Person(id=4, name="Claire", surname="Johnson", admin=False, email="claire@example.com", phone_number="555666777")
        self.qual = PersonRoleQualification(person=person, role=role, category=category, qualified=True)

    def test_person_role_qualification_creation(self):
        self.assertTrue(self.qual.qualified)
        self.assertEqual(self.qual.role.name, "Speaker")

    def test_person_role_qualification_set_qualified(self):
        self.qual.set_qualified(False)
        self.assertFalse(self.qual.qualified)
