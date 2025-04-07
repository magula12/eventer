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


class TestInfeasibilityDiagnostics(unittest.TestCase):

    def test_ilp_diagnose_insufficient_users(self):
        # One issue needs 2 Režisérs, only 1 available
        issues = [
            Issue({
                "id": 1,
                "subject": "Test Event",
                "category": "Hokej SHL",
                "category_priority": "High",
                "priority": "High",
                "start_datetime": "2025-03-29T15:00:00",
                "required_roles": [
                    {"role": "Režisér", "required_count": 2, "assigned_users": []}
                ]
            })
        ]

        users = [
            User({
                "id": 1,
                "firstname": "Only",
                "lastname": "Director",
                "qualifications": [{"role": "Režisér", "category": "Hokej SHL", "rating": 10}],
                "off_days": [],
                "custom_filters": []
            })
        ]

        print("\n=== TEST OUTPUT: ILP DIAGNOSE ===")
        # Run the actual algorithm (will be infeasible)
        result = match_issues_to_users(issues, users)

        # The ILP result should be empty due to infeasibility
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
