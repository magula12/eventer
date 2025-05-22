import unittest
import sys
import os
from datetime import datetime, timedelta
import time

# Ensure the parent directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users

class TestCrossCategorySwap(unittest.TestCase):
    """ILP‑only solvable assignment; measures runtime & coverage."""

    def setUp(self):
        start1 = datetime(2025, 3, 7, 18, 0)
        start2 = datetime(2025, 3, 7, 18, 30)

        # Two issues, one technician needed each.
        self.issues = [
            Issue({
                "id": 1,
                "subject": "A‑Issue",
                "category": "A",
                "category_priority": None,
                "priority": "High",
                "start_datetime": start1.isoformat(),
                "end_datetime": (start1 + timedelta(hours=2)).isoformat(),
                "required_roles": [
                    {"role": "Technician", "required_count": 1, "assigned_users": []}
                ],
            }),
            Issue({
                "id": 2,
                "subject": "B‑Issue",
                "category": "B",
                "category_priority": None,
                "priority": "High",
                "start_datetime": start2.isoformat(),
                "end_datetime": (start2 + timedelta(hours=2)).isoformat(),
                "required_roles": [
                    {"role": "Technician", "required_count": 1, "assigned_users": []}
                ],
            }),
        ]

        # One star user (id 1) who can handle both categories; one support
        # user (id 2) who can handle only category A.
        self.users = [
            User({
                "id": 1,
                "firstname": "Star",
                "lastname": "User",
                "qualifications": [
                    {"role": "Technician", "category": "A", "rating": 10},
                    {"role": "Technician", "category": "B", "rating": 10},
                ],
                "off_days": [],
                "custom_filters": [],
            }),
            User({
                "id": 2,
                "firstname": "Support",
                "lastname": "User",
                "qualifications": [
                    {"role": "Technician", "category": "A", "rating": 8},
                ],
                "off_days": [],
                "custom_filters": [],
            }),
        ]

        self.total_required_slots = 2  # 1 role per issue × 2 issues

    # Helper -------------------------------------------------------------
    def coverage_percent(self, result):
        filled = sum(len(uids)
                     for issue_roles in result.values()
                     for uids in issue_roles.values())
        return 100.0 * filled / self.total_required_slots

    # Test ---------------------------------------------------------------
    def test_only_ilp_finds_solution(self):
        expected_ilp = {
            1: {"Technician": [2]},  # User 2 handles category A
            2: {"Technician": [1]},  # User 1 reserved for category B
        }

        strategies = [
            ("ilp", expected_ilp),
            ("greedy", {1: {"Technician": [1]}, 2: {"Technician": []}}),
            ("backtracking_basic", {}),("smart_greedy", {1: {'Technician': [1]}, 2: {'Technician': []}}),

        ]

        print()  # blank line before metrics table
        for name, expected in strategies:
            t0 = time.perf_counter_ns()
            result = match_issues_to_users(
                self.issues,
                self.users,
                allow_partial=False,
                strategy=name,
            )
            runtime_ms = (time.perf_counter_ns() - t0) / 1_000_000
            cov = self.coverage_percent(result)
            print(f"{name.upper():18s} runtime = {runtime_ms:9.3f} ms | "
                  f"coverage = {cov:6.1f}%")

            # Behavioural assertion
            self.assertEqual(result, expected,
                             f"{name} produced an unexpected assignment")

        # Extra coverage sanity checks
        self.assertEqual(self.coverage_percent(expected_ilp), 100.0)
        self.assertLess(self.coverage_percent(strategies[1][1]), 100.0)  # greedy < 100%
        self.assertLess(self.coverage_percent(strategies[2][1]), 100.0)  # backtracking < 100%


if __name__ == "__main__":
    unittest.main()
