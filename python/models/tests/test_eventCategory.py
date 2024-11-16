import unittest

from ..eventCategory import EventCategory

class TestEventCategory(unittest.TestCase):
    def setUp(self):
        self.category = EventCategory(id=1, techName="Music", description="Music events", priority=2)

    def test_event_category_creation(self):
        self.assertEqual(self.category.techName, "Music")
        self.assertEqual(self.category.description, "Music events")
        self.assertEqual(self.category.priority, 2)

    def test_event_category_str_repr(self):
        self.assertEqual(str(self.category), "Music (2)")
        self.assertEqual(repr(self.category), "Music (2)")

    def test_event_category_comparison(self):
        category_high = EventCategory(id=2, techName="Art", description="Art events", priority=3)
        self.assertTrue(self.category < category_high)
        self.assertFalse(self.category > category_high)
        self.assertTrue(self.category <= category_high)
        self.assertTrue(self.category != category_high)

    def test_event_category_setters_getters(self):
        self.category.set_techName("New Music")
        self.category.set_description("Updated description")
        self.category.set_priority(5)
        self.assertEqual(self.category.get_techName(), "New Music")
        self.assertEqual(self.category.get_description(), "Updated description")
        self.assertEqual(self.category.get_priority(), 5)
