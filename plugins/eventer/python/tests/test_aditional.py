import unittest
import sys
import os
from datetime import datetime

# Ensure the parent directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users

class AditionalTests(unittest.TestCase):
    def test_unsolvable_three_issues_same_day(self):
        """Three issues on the same day, not enough unique qualified users to cover all roles."""
        issues = [
            Issue({
                "id": 33,
                "subject": "Piestanske Cajky - CBK Samorin 2",
                "start_datetime": "2025-03-27T10:00:00",
                "end_datetime": "2025-03-27T13:30:00",
                "category": "Basket EXZ",
                "category_priority": None,
                "priority": "Normálna",
                "required_roles": [
                    {"role": "Režisér", "required_count": 1,
                     "assigned_users": [{"id": 6, "firstname": "Martin", "lastname": "Duri"}]},
                    {"role": "Komentátor", "required_count": 1,
                     "assigned_users": [{"id": 10, "firstname": "Sajmon", "lastname": "Bacista"}]}
                ]
            }),
            Issue({
                "id": 32,
                "subject": "Piestanske Cajky - CBK Samorin",
                "start_datetime": "2025-03-27T13:00:00",
                "category": "Basket EXZ",
                "category_priority": None,
                "priority": "Normálna",
                "required_roles": [
                    {"role": "Režisér", "required_count": 1, "assigned_users": []},
                    {"role": "Komentátor", "required_count": 1, "assigned_users": []}
                ]
            }),
            Issue({
                "id": 34,
                "subject": "Košice - Nové Zámky",
                "start_datetime": "2025-03-27T12:00:00",
                "category": "Hokej Extraliga",
                "category_priority": None,
                "priority": "Normálna",
                "required_roles": [
                    {"role": "Režisér", "required_count": 1, "assigned_users": []},
                    {"role": "Komentátor", "required_count": 1, "assigned_users": []}
                ]
            })
        ]

        users = [
            User({
                "id": 6,
                "login": "mduri",
                "firstname": "Martin",
                "lastname": "Duri",
                "qualifications": [
                    {"role": "Režisér", "category": "Hokej SHL", "rating": 6},
                    {"role": "Režisér", "category": "Basket EXZ", "rating": 4},
                    {"role": "Režisér", "category": "Hokej Extraliga", "rating": 4}
                ],
                "off_days": []
            }),
            User({
                "id": 5,
                "login": "ateski",
                "firstname": "Adam",
                "lastname": "Teski",
                "qualifications": [
                    {"role": "Režisér", "category": "Hokej Extraliga", "rating": 9},
                    {"role": "Režisér", "category": "Hokej SHL", "rating": 7},
                    {"role": "Režisér", "category": "Basket EXZ", "rating": 5}
                ],
                "off_days": []
            }),
            User({
                "id": 9,
                "login": "abuksa",
                "firstname": "Andrej",
                "lastname": "Buksa",
                "qualifications": [
                    {"role": "Komentátor", "category": "Hokej SHL", "rating": 7},
                    {"role": "Komentátor", "category": "Hokej Extraliga", "rating": 1},
                    {"role": "Komentátor", "category": "Basket EXZ", "rating": 4}
                ],
                "off_days": []
            }),
            User({
                "id": 10,
                "login": "sbacista",
                "firstname": "Sajmon",
                "lastname": "Bacista",
                "qualifications": [
                    {"role": "Komentátor", "category": "Basket EXZ", "rating": 1}
                ],
                "off_days": []
            })
        ]

        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {}, "Expected no solution due to role conflicts and already assigned users.")


if __name__ == '__main__':
    unittest.main()
