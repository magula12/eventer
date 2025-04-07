import os
import sys
import unittest
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users

from helper import parse_datetime
from filter_eval import evaluate_filter_block


class AdditionalMatchingEdgeCases(unittest.TestCase):

    def test_missing_end_datetime_defaults(self):
        """Issue with no end_datetime should default to +3 hours."""
        issue = Issue({
            "id": 1,
            "subject": "Test Issue",
            "category": "General",
            "category_priority": None,
            "priority": "High",
            "start_datetime": "2025-03-07T10:00:00",
            "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
        })
        self.assertIsNotNone(issue.end_datetime)
        self.assertEqual(issue.end_datetime.hour, 13)

    def test_same_user_for_multiple_roles_conflict(self):
        """User should not be double-assigned to two roles on the same issue."""

        issues = [Issue({
            "id": 2,
            "subject": "Dual Role Test",
            "category": "General",
            "category_priority": None,
            "priority": "High",
            "start_datetime": "2025-03-07T12:00:00",
            "end_datetime": "2025-03-07T13:00:00",
            "required_roles": [
                {"role": "Director", "required_count": 1, "assigned_users": []},
                {"role": "Commentator", "required_count": 1, "assigned_users": []}
            ]
        })]

        users = [User({
            "id": 1,
            "firstname": "User",
            "lastname": "Multi",
            "qualifications": [
                {"role": "Director", "category": "General", "rating": 9},
                {"role": "Commentator", "category": "General", "rating": 8}
            ]
        })]

        results = match_issues_to_users(issues, users)

        if results == {}:
            print("✅ ILP correctly marked it infeasible due to role conflict on single issue.")
            self.assertEqual(results, {})
        else:
            assigned_roles = results.get(2, {})
            assigned_user_ids = []
            for user_ids in assigned_roles.values():
                assigned_user_ids.extend(user_ids)
            # User should not be assigned more than once across different roles
            self.assertEqual(assigned_user_ids.count(1), 1)

    def test_user_wrong_category(self):
        """User is not qualified for the issue's category."""
        issues = [Issue({
            "id": 3,
            "subject": "Wrong Category",
            "category": "Basketball",
            "category_priority": None,
            "priority": "Medium",
            "start_datetime": "2025-03-07T14:00:00",
            "required_roles": [{"role": "Referee", "required_count": 1, "assigned_users": []}]
        })]
        users = [User({
            "id": 1,
            "firstname": "Wrong",
            "lastname": "Category",
            "qualifications": [{"role": "Referee", "category": "Football", "rating": 10}]
        })]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {})

    def test_conflicting_issues_user_only_available_for_one(self):
        """User should only be assigned to one of two overlapping issues."""

        issues = [
            Issue({
                "id": 4,
                "subject": "Conflict 1",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": "2025-03-07T10:00:00",
                "end_datetime": "2025-03-07T12:00:00",
                "required_roles": [{"role": "Judge", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 5,
                "subject": "Conflict 2",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": "2025-03-07T11:30:00",
                "end_datetime": "2025-03-07T13:30:00",
                "required_roles": [{"role": "Judge", "required_count": 1, "assigned_users": []}]
            })
        ]

        users = [User({
            "id": 1,
            "firstname": "Busy",
            "lastname": "Person",
            "qualifications": [{"role": "Judge", "category": "General", "rating": 10}]
        })]

        results = match_issues_to_users(issues, users)

        if results == {}:
            print("✅ ILP detected infeasibility — user can't cover both overlapping issues.")
            # Assert that result is indeed empty as expected
            self.assertEqual(results, {})
        else:
            # In case fallback algorithm was used
            assigned_count = sum(len(v.get("Judge", [])) for v in results.values())
            self.assertEqual(assigned_count, 1)

    def test_lower_rated_user_fallback(self):
        """Lower rated user should be selected if higher rated is unavailable."""
        issues = [Issue({
            "id": 6,
            "subject": "Fallback Test",
            "category": "General",
            "category_priority": None,
            "priority": "High",
            "start_datetime": "2025-03-07T18:00:00",
            "required_roles": [{"role": "Technician", "required_count": 1, "assigned_users": []}]
        })]
        users = [
            User({
                "id": 1,
                "firstname": "Unavailable",
                "lastname": "HighRating",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 10}],
                "off_days": [{"start_datetime": "2025-03-07T17:00:00", "end_datetime": "2025-03-07T19:00:00"}]
            }),
            User({
                "id": 2,
                "firstname": "Available",
                "lastname": "LowRating",
                "qualifications": [{"role": "Technician", "category": "General", "rating": 6}],
                "off_days": []
            })
        ]
        results = match_issues_to_users(issues, users)
        self.assertEqual(results, {6: {"Technician": [2]}})


if __name__ == "__main__":
    unittest.main()
