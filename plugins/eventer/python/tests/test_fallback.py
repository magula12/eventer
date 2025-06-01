"""test_fallback.py

A test case demonstrating fallback behavior where ILP fails to find a solution
(0% coverage) but Greedy can still make some assignments.

Key points
~~~~~~~~~~
* Creates a scenario where multiple users are required per issue
* Not enough users are available to satisfy all requirements
* ILP fails to find a solution while Greedy can make partial assignments
* Greedy ignores allow_partial and always makes partial assignments when needed
* Backtracking should also fail like ILP since it requires complete solutions
"""

from __future__ import annotations

import os
import sys
import time as time_module
import unittest
from datetime import datetime, timedelta, time
from typing import Dict, List

# ---------------------------------------------------------------------------
# Import system under test
# ---------------------------------------------------------------------------
THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from models import Issue, User  # type: ignore
from process import match_issues_to_users  # type: ignore

# ---------------------------------------------------------------------------
# Synthetic data builders
# ---------------------------------------------------------------------------

ISSUE_SPACING_MINUTES = 15  # new issue every 15 min (more overlap)
ISSUE_DURATION_HOURS = 2    # each issue lasts 2 h
NUM_ISSUES = 25            # 25 issues
USERS_PER_ISSUE = 2        # each issue needs 2 users
TOTAL_USERS = 8            # only 8 users available (not enough for overlapping issues)


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
    
    # Create only TOTAL_USERS when we need NUM_ISSUES * USERS_PER_ISSUE
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
                    "off_days": [],  # No off days to keep it simple
                    "custom_filters": [],  # No time filters to keep it simple
                }
            )
        )
    
    return users


# ---------------------------------------------------------------------------
# TestCase
# ---------------------------------------------------------------------------


class TestFallbackBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_start = datetime(2025, 3, 7, 9, 0)  # Start at 9:00
        cls.issues = build_issues(base_start)
        cls.users = build_users()
        # Calculate total required users
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
            allow_partial=False,  # Don't allow partial assignments
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

        # ILP should fail to find a solution
        self.assertEqual(metrics["ilp"][1], 0.0, "ILP should fail to find any assignments")
        
        # Backtracking should also fail since it requires complete solutions
        self.assertEqual(metrics["backtracking_basic"][1], 0.0, "Backtracking should fail to find any assignments")
        
        # Greedy should make partial assignments regardless of allow_partial
        self.assertGreater(metrics["greedy"][1], 0.0, "Greedy should make partial assignments")
        
        # Greedy should find more assignments than ILP and Backtracking
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