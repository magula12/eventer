import unittest

from ..role import Role

class TestRole(unittest.TestCase):
    def setUp(self):
        self.role = Role(id=1, name="Director", priority=3)

    def test_role_creation(self):
        self.assertEqual(self.role.name, "Director")
        self.assertEqual(self.role.priority, 3)

    def test_role_str_repr(self):
        self.assertEqual(str(self.role), "Director")
        self.assertEqual(repr(self.role), "Director")

    def test_role_setters_getters(self):
        self.role.set_name("Sound Engineer")
        self.role.set_priority(2)
        self.assertEqual(self.role.get_name(), "Sound Engineer")
        self.assertEqual(self.role.get_priority(), 2)

    def test_role_comparison(self):
        role_lower = Role(id=2, name="Assistant", priority=1)
        self.assertTrue(self.role > role_lower)
        self.assertFalse(self.role < role_lower)
