"""test_massive_issue_assignment.py

A *stress‑test* and **benchmark** for `match_issues_to_users` that prints
both runtime (high‑precision) and coverage for several strategies.

Key points
~~~~~~~~~~
* 24 issues, staggered every 30 minutes, 2‑hour duration → up to 4
  concurrent technicians required.
* Three “valid” users with non‑overlapping time‑window soft filters; four
  high‑rating users with an impossible category filter (also soft).
* Hard constraints: no overlapping assignments, no off‑day clashes, must
  be qualified.

Expected results
----------------
* **ILP** can ignore soft filters at a cost → **100 % coverage**.
* **Greedy** and **Basic Backtracking** treat filters as hard and will
  miss slots (<100 % coverage).

This file also measures runtime with µs‑level precision so even very fast
algorithms (>0 µs) show non‑zero times.
"""

from __future__ import annotations

import os
import sys
import time
import unittest
from datetime import datetime, timedelta
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

ISSUE_SPACING_MINUTES = 30  # new issue every 30 min
ISSUE_DURATION_HOURS = 2    # each issue lasts 2 h ⇒ max 4 overlap
NUM_ISSUES = 24             # 12 h horizon


def build_issues(start_dt: datetime) -> List[Issue]:
    """Generate *NUM_ISSUES* issues staggered by ISSUE_SPACING_MINUTES."""
    issues: List[Issue] = []
    for i in range(NUM_ISSUES):
        s = start_dt + timedelta(minutes=i * ISSUE_SPACING_MINUTES)
        e = s + timedelta(hours=ISSUE_DURATION_HOURS)
        issues.append(
            Issue(
                {
                    "id": i + 1,
                    "subject": f"Issue {i + 1}",
                    "category": "General",  # every user qualified
                    "category_priority": None,
                    "priority": "High",
                    "start_datetime": s.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_datetime": e.strftime("%Y-%m-%dT%H:%M:%S"),
                    "required_roles": [
                        {"role": "Technician", "required_count": 1, "assigned_users": []}
                    ],
                }
            )
        )
    return issues


# Three "valid" users – exactly **one** passes filters for any issue.
# Four high‑rating users – filters never pass (category == "Z").

TIME_FILTER_DEFS = [
    ("<", "2025-03-07T20:00:00"),
    ("between", ("2025-03-07T20:00:00", "2025-03-07T22:00:00")),
    (">=", "2025-03-07T22:00:00"),
]


def _build_time_filter(op: str, val):
    """Return a JSONLogic‑like dict expressing a `start_time` condition."""
    if op == "<":
        cmp_time = datetime.fromisoformat(val).time()
        return {"rules": {"and": [{"<": [{"var": "start_time"}, cmp_time]}]}}
    if op == ">=":
        cmp_time = datetime.fromisoformat(val).time()
        return {"rules": {"and": [{">=": [{"var": "start_time"}, cmp_time]}]}}
    # op == "between"
    low_iso, high_iso = val  # type: ignore[misc]
    low, high = datetime.fromisoformat(low_iso).time(), datetime.fromisoformat(high_iso).time()
    return {
        "rules": {
            "and": [
                {">=": [{"var": "start_time"}, low]},
                {"<": [{"var": "start_time"}, high]},
            ]
        }
    }


def build_users() -> List[User]:
    users: List[User] = []

    # Users 1‑3: valid, mutually exclusive time windows, rating 6
    for uid, (op, val) in enumerate(TIME_FILTER_DEFS, start=1):
        users.append(
            User(
                {
                    "id": uid,
                    "firstname": f"User{uid}",
                    "lastname": "Valid",
                    "qualifications": [
                        {"role": "Technician", "category": "General", "rating": 6},
                    ],
                    "off_days": [],
                    "custom_filters": [
                        {
                            "name": "TimeFilter",
                            "conditions": _build_time_filter(op, val),
                        }
                    ],
                }
            )
        )

    # Users 4‑7: high rating 10, impossible category filter (soft)
    for uid in range(4, 8):
        users.append(
            User(
                {
                    "id": uid,
                    "firstname": f"User{uid}",
                    "lastname": "Penalty",
                    "qualifications": [
                        {"role": "Technician", "category": "General", "rating": 10},
                    ],
                    "off_days": [],
                    "custom_filters": [
                        {
                            "name": "BadCategory",
                            "conditions": {
                                "rules": {
                                    "and": [
                                        {"==": [{"var": "category"}, "Z"]},  # never true
                                    ]
                                }
                            },
                        }
                    ],
                }
            )
        )
    return users


# ---------------------------------------------------------------------------
# TestCase
# ---------------------------------------------------------------------------


class TestMassiveIssueAssignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_start = datetime(2025, 3, 7, 18, 0)
        cls.issues = build_issues(base_start)
        cls.users = build_users()
        # Each issue demands exactly one Technician
        cls.total_required = len(cls.issues)

    # ------------------------------ utilities ------------------------------

    def _coverage(self, result: Dict[int, Dict[str, List[int]]]) -> float:
        """Return filled‑slot fraction (0‑1)."""
        filled = sum(
            len(uids) for role_map in result.values() for uids in role_map.values()
        )
        return filled / self.total_required

    def _run_strategy(self, strategy: str):
        t0 = time.perf_counter()
        result = match_issues_to_users(
            self.issues,
            self.users,
            allow_partial=False,
            strategy=strategy,
        )
        elapsed = time.perf_counter() - t0
        return elapsed, self._coverage(result), result

    # ------------------------------ tests ----------------------------------

    def test_ilp_vs_heuristics(self):
        """ILP must hit 100 % coverage; greedy/backtracking must not."""
        strategies = ["ilp", "greedy", "backtracking_basic"]
        metrics = {}
        for s in strategies:
            runtime, cov, _ = self._run_strategy(s)
            metrics[s] = (runtime, cov)
            # Print with µs‑level precision so very fast calls aren't shown as 0.0 ms
            print(
                f"{s.upper():<18} runtime = {runtime * 1000:9.3f} ms | coverage = {cov * 100:6.1f}%"
            )

        self.assertEqual(metrics["ilp"][1], 1.0, "ILP should fully cover all roles")
        self.assertLess(metrics["greedy"][1], 1.0, "Greedy should not cover all roles")
        self.assertEqual(
            metrics["backtracking_basic"][1], 1.0, "Backtracking should not cover all roles"
        )

    def test_positive_runtime_all(self):
        """All strategies should take >0 s (runtime measurement sanity)."""
        for strategy in ["ilp", "greedy", "backtracking_basic"]:
            rt, _, _ = self._run_strategy(strategy)
            self.assertGreater(rt, 0, f"{strategy} runtime not positive")

if __name__ == "__main__":
    unittest.main()
