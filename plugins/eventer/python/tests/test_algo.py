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
        self.assertEqual(results, {})

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
        self.assertEqual(results, {})

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
        """User cannot be assigned to two overlapping issues (ILP returns {} if infeasible)."""
        issues = [
            Issue({
                "id": 2, "subject": "Issue 2", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T12:00:00",
                "end_datetime": "2025-03-07T13:00:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 3, "subject": "Issue 3", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T12:30:00",  # Overlaps with Issue 2
                "end_datetime": "2025-03-07T13:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            })
        ]

        users = [User({
            "id": 1, "firstname": "Test", "lastname": "User",
            "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
        })]

        results = match_issues_to_users(issues, users)

        if results == {}:
            print("✅ Test passed: ILP correctly found overlapping assignments infeasible.")
            self.assertEqual(results, {})  # Optional explicit check
        else:
            # Defensive fallback: if fallback solver was used (e.g., greedy), ensure no double booking
            assignments = []
            for issue_id in [2, 3]:
                assigned = results.get(issue_id, {}).get("Director", [])
                assignments.extend(assigned)
            self.assertLessEqual(assignments.count(1), 1, "User was assigned to overlapping issues!")

    def test_user_assigned_only_when_no_conflict(self):
        """User is assigned only when there is no time conflict. ILP returns {} if infeasible."""
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
                "start_datetime": "2025-03-07T15:00:00",  # Overlaps with previous
                "end_datetime": "2025-03-07T16:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            }),
            Issue({
                "id": 6, "subject": "Issue 6", "category": "General",
                "category_priority": None, "priority": "High",
                "start_datetime": "2025-03-07T16:00:00",  # Overlaps with previous
                "end_datetime": "2025-03-07T17:30:00",
                "required_roles": [{"role": "Director", "required_count": 1, "assigned_users": []}]
            })
        ]

        users = [User({
            "id": 1, "firstname": "Test", "lastname": "User",
            "qualifications": [{"role": "Director", "category": "General", "rating": 9}]
        })]

        results = match_issues_to_users(issues, users)

        # If infeasible, ILP returns {}, so just confirm that
        if results == {}:
            print("⚠️ ILP correctly detected infeasibility due to overlapping roles and limited users.")
            self.assertEqual(results, {})  # Optional, explicit confirmation
        else:
            # If partial solution is enabled or another algorithm is used
            # still validate no double assignment
            assignments = []
            for issue_id in [4, 5, 6]:
                assigned = results.get(issue_id, {}).get("Director", [])
                assignments.extend(assigned)

            # Ensure user 1 is not assigned to multiple overlapping issues
            self.assertLessEqual(assignments.count(1), 1)

    def test_forward_assignments_respected(self):
        """Test that forward assignments are respected and not overwritten."""
        issues = [
            Issue({
                "id": 7,
                "subject": "Forward Assignment Test",
                "category": "General",
                "category_priority": None,
                "priority": "High",
                "start_datetime": "2025-03-07T20:00:00",
                "end_datetime": "2025-03-07T21:00:00",
                "required_roles": [
                    {
                        "role": "Director",
                        "required_count": 2,
                        "assigned_users": [
                            {"id": 1, "firstname": "Forward", "lastname": "Assigned"}
                        ]
                    }
                ]
            })
        ]

        users = [
            User({
                "id": 1,
                "firstname": "Forward",
                "lastname": "Assigned",
                "qualifications": [{"role": "Director", "category": "General", "rating": 8}]
            }),
            User({
                "id": 2,
                "firstname": "Higher",
                "lastname": "Rating",
                "qualifications": [{"role": "Director", "category": "General", "rating": 10}]
            })
        ]

        # Test ILP strategy
        results_ilp = match_issues_to_users(issues, users, strategy="ilp")
        self.assertIn(1, results_ilp[7]["Director"], "Forward assigned user should be in ILP results")
        self.assertIn(2, results_ilp[7]["Director"], "Higher rated user should also be assigned in ILP")
        self.assertEqual(len(results_ilp[7]["Director"]), 2, "Should have exactly 2 assigned users in ILP")

        # Test Greedy strategy
        results_greedy = match_issues_to_users(issues, users, strategy="greedy")
        self.assertIn(1, results_greedy[7]["Director"], "Forward assigned user should be in Greedy results")
        self.assertIn(2, results_greedy[7]["Director"], "Higher rated user should also be assigned in Greedy")
        self.assertEqual(len(results_greedy[7]["Director"]), 2, "Should have exactly 2 assigned users in Greedy")


if __name__ == "__main__":
    start = datetime.now()
    unittest.main()
    print("Time taken: ", datetime.now() - start)
