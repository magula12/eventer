import unittest
import sys
import os
from datetime import datetime

# Ensure the parent directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users


class IssueUserMatchingTests(unittest.TestCase):

    def test_no_issues_no_users(self):
        """No issues and no users."""
        issues = []
        users = []
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {})

    def test_issues_without_required_roles(self):
        """Issues that do not require roles."""
        issues = [Issue({
            "id": 1, "subject": "Issue 1", "category": "General",
            "category_priority": None, "priority": "Medium",
            "start_datetime": "2025-03-07T10:00:00",  # Ensuring start_datetime is present
            "required_roles": []
        })]
        users = [User({"id": 1, "firstname": "Test", "lastname": "User", "qualifications": []})]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {1: {}})

    def test_issues_with_roles_but_no_users(self):
        """Issues require roles, but no users available."""
        issues = [Issue({
            "id": 2, "subject": "Issue 2", "category": "General",
            "category_priority": None, "priority": "High",
            "start_datetime": "2025-03-07T11:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })]
        users = []
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {2: {"Director": []}})

    def test_single_issue_single_user_exact_match(self):
        """Single issue with a user who exactly matches the role."""
        issues = [Issue({
            "id": 3, "subject": "Issue 3", "category": "General",
            "category_priority": None, "priority": "High",
            "start_datetime": "2025-03-07T12:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })]
        users = [User({
            "id": 1, "firstname": "Test", "lastname": "User",
            "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
        })]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {3: {"Director": [1]}})

    def test_multiple_users_one_role_best_fit(self):
        """Multiple users available, best rating wins."""
        issues = [Issue({
            "id": 4, "subject": "Issue 4", "category": "General",
            "category_priority": None, "priority": "Low",
            "start_datetime": "2025-03-07T14:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })]
        users = [
            User({
                "id": 1, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 7}]
            }),
            User({
                "id": 2, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
            })
        ]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {4: {"Director": [2]}})

    def test_user_not_available_due_to_off_day(self):
        """User is unavailable because of an off-day."""
        issues = [Issue({
            "id": 5, "subject": "Issue 5", "category": "General",
            "category_priority": None, "priority": "High",
            "start_datetime": "2025-03-07T16:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })]
        users = [
            User({
                "id": 1, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 9}],
                "off_days": [{"start_datetime": "2025-03-07T15:00:00", "end_datetime": "2025-03-07T17:00:00"}]
            })
        ]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {5: {"Director": []}})

    def test_multiple_roles_multiple_users(self):
        """Matching multiple users to multiple roles."""
        issues = [Issue({
            "id": 6, "subject": "Issue 6", "category": "General",
            "category_priority": None, "priority": "Medium",
            "start_datetime": "2025-03-07T18:00:00",
            "required_roles": [
                {"role": "Director", "required_count": 1, "assigned_users": []},
                {"role": "Commentator", "required_count": 1, "assigned_users": []}
            ]
        })]
        users = [
            User({
                "id": 1, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 8}]
            }),
            User({
                "id": 2, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Commentator", "category": "General", "rating": 9}]
            })
        ]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {6: {"Director": [1], "Commentator": [2]}})

    def test_users_with_same_rating(self):
        """If two users have the same rating, tie-breaking should be consistent."""
        issues = [Issue({
            "id": 7, "subject": "Issue 7", "category": "General",
            "category_priority": None, "priority": "High",
            "start_datetime": "2025-03-07T20:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })]
        users = [
            User({
                "id": 1, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 8}]
            }),
            User({
                "id": 2, "firstname": "Test", "lastname": "User",
                "qualifications": [{"role": "Director", "category": "General", "rating": 8}]
            })
        ]
        results = match_issues_to_users(issues, users)
        self.assertTrue(results[7]["Director"][0] in [1, 2])  # Either user should be assigned

    def test_user_cannot_be_double_booked(self):
        """User cannot be assigned to two issues that overlap in time."""
        issues = [
            Issue({
                "id": 2, "subject": "Issue 2", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T12:00:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 3, "subject": "Issue 3", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T12:30:00",  # Overlaps with Issue 2
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            })
        ]
        users = [User({
            "id": 1, "firstname": "Test", "lastname": "User",
            "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
        })]

        results = match_issues_to_users(issues, users)
        self.assertNotEqual(results[2]["Director"], results[3]["Director"])  # Ensure different users are assigned

    def test_user_assigned_only_when_no_conflict(self):
        """User is assigned sequentially where each task starts 30 min before the previous one ends."""
        issues = [
            Issue({
                "id": 4, "subject": "Issue 4", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T14:00:00",
                "end_datetime": "2025-03-07T15:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 5, "subject": "Issue 5", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T15:00:00",  # Starts 30 min before previous one ends
                "end_datetime": "2025-03-07T16:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 6, "subject": "Issue 6", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T16:00:00",  # Starts 30 min before previous one ends
                "end_datetime": "2025-03-07T17:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            })
        ]
        users = [User({
            "id": 1, "firstname": "Test", "lastname": "User",
            "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
        })]

        results = match_issues_to_users(issues, users)
        self.assertNotEqual(results[4]["Director"], results[5]["Director"])  # Ensure different users are assigned
        self.assertNotEqual(results[5]["Director"], results[6]["Director"])

if __name__ == "__main__":
    start = datetime.now()
    unittest.main()
    print("Time taken: ", datetime.now() - start)
