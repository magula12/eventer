from __future__ import annotations

import os
import sys
import time as time_module
import unittest
from datetime import datetime, timedelta, time
from typing import Dict, List

THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from models import Issue, User
from process import match_issues_to_users


ISSUE_SPACING_MINUTES = 15 
ISSUE_DURATION_HOURS = 2 
NUM_ISSUES = 25
USERS_PER_ISSUE = 2 
TOTAL_USERS = 8


def build_issues(start_dt: datetime) -> List[Issue]:
    """Generate issues requiring multiple users with high overlap."""
    issues: List[Issue] = []
    for i in range(NUM_ISSUES):
        s = start_dt + timedelta(minutes=i * ISSUE_SPACING_MINUTES)
        e = s + timedelta(hours=ISSUE_DURATION_HOURS)
        issues.append(
            Issue(
                {
                    "id": i + 1,
                    "subject": f"Issue {i + 1}",
                    "category": "General",
                    "category_priority": None,
                    "priority": "High",
                    "start_datetime": s.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_datetime": e.strftime("%Y-%m-%dT%H:%M:%S"),
                    "required_roles": [
                        {"role": "Technician", "required_count": USERS_PER_ISSUE, "assigned_users": []}
                    ],
                }
            )
        )
    return issues


def build_users() -> List[User]:
    """Create a limited number of users that can't satisfy all requirements."""
    users: List[User] = []
    
    for uid in range(1, TOTAL_USERS + 1):
        users.append(
            User(
                {
                    "id": uid,
                    "firstname": f"User{uid}",
                    "lastname": "Limited",
                    "qualifications": [
                        {"role": "Technician", "category": "General", "rating": 5},
                    ],
                    "off_days": [],
                    "custom_filters": [],
                }
            )
        )
    
    return users

class TestFallbackBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_start = datetime(2025, 3, 7, 9, 0)  # Start at 9:00
        cls.issues = build_issues(base_start)
        cls.users = build_users()
        cls.total_required = sum(
            role.required_count 
            for issue in cls.issues 
            for role in issue.required_roles
        )
        print(f"\nTest setup:")
        print(f"- {NUM_ISSUES} issues, each requiring {USERS_PER_ISSUE} users")
        print(f"- Total required users: {cls.total_required}")
        print(f"- Available users: {TOTAL_USERS}")
        print(f"- Issue duration: {ISSUE_DURATION_HOURS}h, spacing: {ISSUE_SPACING_MINUTES}min")

    def _coverage(self, result: Dict[int, Dict[str, List[int]]]) -> float:
        """Return filled‑slot fraction (0‑1)."""
        filled = sum(
            len(uids) for role_map in result.values() for uids in role_map.values()
        )
        return filled / self.total_required

    def _run_strategy(self, strategy: str):
        t0 = time_module.perf_counter()
        result = match_issues_to_users(
            self.issues,
            self.users,
            allow_partial=False,
            strategy=strategy,
        )
        elapsed = time_module.perf_counter() - t0
        return elapsed, self._coverage(result), result

    def test_ilp_fails_greedy_succeeds(self):
        """ILP and Backtracking should fail (0% coverage) while Greedy can make some assignments."""
        strategies = ["ilp", "greedy", "backtracking_basic"]
        metrics = {}
        
        for s in strategies:
            runtime, cov, _ = self._run_strategy(s)
            metrics[s] = (runtime, cov)
            print(
                f"{s.upper():<18} runtime = {runtime * 1000:9.3f} ms | coverage = {cov * 100:6.1f}%"
            )

        self.assertEqual(metrics["ilp"][1], 0.0, "ILP should fail to find any assignments")
        
        self.assertEqual(metrics["backtracking_basic"][1], 0.0, "Backtracking should fail to find any assignments")
        
        self.assertGreater(metrics["greedy"][1], 0.0, "Greedy should make partial assignments")
        
        self.assertGreater(
            metrics["greedy"][1],
            metrics["ilp"][1],
            "Greedy should find more assignments than ILP"
        )
        self.assertGreater(
            metrics["greedy"][1],
            metrics["backtracking_basic"][1],
            "Greedy should find more assignments than Backtracking"
        )

if __name__ == "__main__":
    unittest.main() 