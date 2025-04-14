import unittest
import sys
import os
from datetime import datetime, timedelta

# Ensure the parent directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users

class TestIssueAssignment(unittest.TestCase):
    def test_only_ilp_solves(self):
        """Test where only ILP finds a solution due to filter violations, while greedy and backtracking fail."""
        # Define issues: two overlapping issues requiring one Technician each
        issue1_start = datetime(2025, 3, 7, 18, 0)  # Issue 1: 18:00–21:00
        issue2_start = datetime(2025, 3, 7, 18, 30)  # Issue 2: 18:30–21:30 (overlaps)
        issues = [
            Issue({
                "id": 1,
                "subject": "Issue 1",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": issue1_start.strftime("%Y-%m-%dT%H:%M:%S"),  # ISO string
                "end_datetime": (issue1_start + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [{"role": "Technician", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 2,
                "subject": "Issue 2",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": issue2_start.strftime("%Y-%m-%dT%H:%M:%S"),  # ISO string
                "end_datetime": (issue2_start + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [{"role": "Technician", "required_count": 1, "assigned_users": []}]
            })
        ]

        # Define users: both qualified, but with conflicting filters and availability
        users = [
            User({
                "id": 1,
                "firstname": "HighRating",
                "lastname": "User1",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 10}],
                "off_days": [],  # Unavailable for Issue 2
                "custom_filters": [{
                    "name": "Filter1",
                    "conditions": {
                        "rules": {
                            "and": [{
                                "==": [
                                    {"var": "category"},
                                    "EXZ"
                                ]
                            }]
                        }
                    }
                }]  # Fails filter for Issue 1 (category != EXZ)
            }),
            User({
                "id": 2,
                "firstname": "LowRating",
                "lastname": "User2",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 6}],
                "off_days": [],
                "custom_filters": [{
                    "name": "Filter2",
                    "conditions": {
                        "rules": {
                            "and": [{
                                "<": [
                                    {"var": "start_time"},
                                    datetime.fromisoformat("2025-03-07T18:15:00").time()
                                ]
                            }]
                        }
                    }
                }]  # Fails filter for Issue 2 (start_time >= 18:15)
            })
        ]

        # Test ILP: Should assign User 2 to Issue 1, User 1 to Issue 2 (despite filter violations)
        ilp_result = match_issues_to_users(issues, users, allow_partial=False, strategy="ilp")
        expected = {
            1: {"Technician": [2]},  # User 2 passes filter for Issue 1
            2: {"Technician": [1]}   # User 1 assigned to Issue 2 despite filter violation
        }
        self.assertEqual(ilp_result, expected, "ILP should find a solution with filter violations")

        # Test Greedy: Should fail (no valid users for Issue 2)
        greedy_result = match_issues_to_users(issues, users, allow_partial=False, strategy="greedy")
        self.assertEqual(greedy_result, {1: {'Technician': [2]}, 2: {'Technician': []}}, "Greedy should fail due to no valid users for Issue 2")

        # Test Backtracking: Should fail (no combination satisfies all filters and availability)
        backtrack_result = match_issues_to_users(issues, users, allow_partial=False, strategy="backtracking_basic")
        self.assertEqual(backtrack_result, {}, "Backtracking should fail due to no valid solution")

    def test_smart_greedy_fails_ilp_succeeds(self):
        """Test where smart greedy fails to assign all roles due to sequential choices and availability, but ILP succeeds."""
        issue1_start = datetime(2025, 3, 7, 18, 0)
        issue2_start = datetime(2025, 3, 7, 18, 30)
        issues = [
            Issue({
                "id": 1,
                "subject": "Issue 1",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": issue1_start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_datetime": (issue1_start + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [{"role": "Technician", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 2,
                "subject": "Issue 2",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": issue2_start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_datetime": (issue2_start + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [{"role": "Technician", "required_count": 1, "assigned_users": []}]
            })
        ]

        users = [
            User({
                "id": 1,
                "firstname": "HighRating",
                "lastname": "User1",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 10}],
                "off_days": [{
                    "start_datetime": "2025-03-07T18:30:00",
                    "end_datetime": "2025-03-07T21:30:00"
                }],
                "custom_filters": [{
                    "name": "Filter1",
                    "conditions": {
                        "rules": {
                            "and": [{
                                "<": [
                                    {"var": "start_time"},
                                    datetime.fromisoformat("2025-03-07T18:15:00").time()
                                ]
                            }]
                        }
                    }
                }]
            }),
            User({
                "id": 2,
                "firstname": "LowRating",
                "lastname": "User2",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 6}],
                "off_days": [],
                "custom_filters": [{
                    "name": "Filter2",
                    "conditions": {
                        "rules": {
                            "and": [{
                                ">=": [
                                    {"var": "start_time"},
                                    datetime.fromisoformat("2025-03-07T19:00:00").time()

                                ]
                            }]
                        }
                    }
                }]
            })
        ]

        ilp_result = match_issues_to_users(issues, users, allow_partial=False, strategy="ilp")
        expected = {
            1: {"Technician": [2]},
            2: {"Technician": [1]}
        }
        self.assertEqual(ilp_result, expected, "ILP should find a complete solution with filter violations")

        greedy_result = match_issues_to_users(issues, users, allow_partial=False, strategy="greedy")
        expected_greedy = {
            1: {"Technician": [1]},
            2: {"Technician": []}
        }
        self.assertEqual(greedy_result, expected_greedy, "Smart greedy should fail to assign Issue 2 due to constraints")

        backtrack_result = match_issues_to_users(issues, users, allow_partial=False, strategy="backtracking_basic")
        self.assertEqual(backtrack_result, {}, "Backtracking should fail due to no valid solution")
if __name__ == "__main__":
    unittest.main()