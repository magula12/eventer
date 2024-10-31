import unittest

from ..person import Person
from ..role import Role

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person(id=1, name="John", surname="Doe", admin=True, email="john@example.com", phone_number="123456789")

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
