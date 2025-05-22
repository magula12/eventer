import unittest
import sys
import os
from datetime import datetime, timedelta
import time
import pulp

# Ensure the parent directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import User, Issue
from process import match_issues_to_users
from algo_backtracking import get_rating, is_time_overlap


class TestBacktrackingFasterThanILP(unittest.TestCase):
    def validate_solution(self, issues, users, result):
        """Validate that the assignment satisfies all constraints."""
        if not result:
            return False, "Empty result"

        # Check all required roles are assigned (up to required_count)
        for issue in issues:
            issue_id = issue.id
            if issue_id not in result:
                return False, f"Issue {issue_id} not assigned"
            assigned_roles = result[issue_id]
            required_roles = {req.role: req.required_count for req in issue.required_roles}
            for role, count in required_roles.items():
                assigned_count = len(assigned_roles.get(role, []))
                if assigned_count > count:
                    return False, f"Issue {issue_id}, Role {role}: Assigned {assigned_count}, Max {count}"
                if assigned_count == 0:
                    return False, f"Issue {issue_id}, Role {role}: No users assigned"

        # Check no multi-role within same issue
        for issue_id, assignments in result.items():
            users_in_issue = []
            for role, user_ids in assignments.items():
                users_in_issue.extend(user_ids)
            if len(users_in_issue) != len(set(users_in_issue)):
                return False, f"Issue {issue_id}: User assigned multiple roles"

        # Check no double-booking across overlapping issues
        issue_times = {
            i.id: (
                i.start_datetime,
                i.end_datetime
            ) for i in issues
        }
        for u in users:
            assigned_issues = []
            for i_id, assignments in result.items():
                for role, user_ids in assignments.items():
                    if u.id in user_ids:
                        assigned_issues.append(i_id)
            for i, i1_id in enumerate(assigned_issues):
                for i2_id in assigned_issues[i + 1:]:
                    s1, e1 = issue_times[i1_id]
                    s2, e2 = issue_times[i2_id]
                    if is_time_overlap(s1, e1, s2, e2):
                        return False, f"User {u.id} double-booked in Issues {i1_id} and {i2_id}"

        # Check qualifications and availability
        for issue_id, assignments in result.items():
            issue = next(i for i in issues if i.id == issue_id)
            start = issue.start_datetime
            end = issue.end_datetime
            for role, user_ids in assignments.items():
                for user_id in user_ids:
                    user = next(u for u in users if u.id == user_id)
                    if get_rating(user, role, issue.category) <= 0:
                        return False, f"User {user_id} unqualified for Role {role} in Issue {issue_id}"
                    for od in user.off_days:
                        od_start = od.start_datetime
                        od_end = od.end_datetime
                        if not (end <= od_start or start >= od_end):
                            return False, f"User {user_id} unavailable for Issue {issue_id}"

        return True, "Valid solution"

    def test_backtracking_faster_than_ilp(self):
        """Test that backtracking is faster than ILP in a simple, unconstrained scenario."""
        base_time = datetime(2025, 4, 10, 8, 0)

        # Define 2 non-overlapping issues with minimal role requirements
        issues = [
            Issue({
                "id": 1,
                "subject": "Issue 1",
                "category": "Network",
                "category_priority": "High",
                "priority": "High",
                "start_datetime": (base_time).strftime("%Y-%m-%dT%H:%M:%S"),
                "end_datetime": (base_time + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [
                    {"role": "Senior Engineer", "required_count": 1, "assigned_users": []},
                    {"role": "Network Specialist", "required_count": 1, "assigned_users": []}
                ]
            }),
            Issue({
                "id": 2,
                "subject": "Issue 2",
                "category": "Network",
                "category_priority": "High",
                "priority": "High",
                "start_datetime": (base_time + timedelta(minutes=70)).strftime("%Y-%m-%dT%H:%M:%S"),
                "end_datetime": (base_time + timedelta(minutes=130)).strftime("%Y-%m-%dT%H:%M:%S"),
                "required_roles": [
                    {"role": "Senior Engineer", "required_count": 1, "assigned_users": []},
                    {"role": "Network Specialist", "required_count": 1, "assigned_users": []}
                ]
            })
        ]

        # Define 10 users, all fully qualified and available
        users = [
            User({
                "id": i + 1,
                "firstname": f"User{i + 1}",
                "lastname": "Test",
                "qualifications": [
                    {"role": "Senior Engineer", "category": "Network", "rating": 8},
                    {"role": "Network Specialist", "category": "Network", "rating": 8}
                ],
                "off_days": [],  # No off-days
                "custom_filters": []
            }) for i in range(10)
        ]

        # Debug: Print eligible users per role per issue
        for issue in issues:
            for role in issue.required_roles:
                start = issue.start_datetime
                end = issue.end_datetime
                eligible = [
                    u for u in users
                    if get_rating(u, role.role, issue.category) > 0 and
                       all(not is_time_overlap(start, end, od.start_datetime, od.end_datetime)
                           for od in u.off_days)
                ]
                print(
                    f"Issue {issue.id}, Role {role.role}, Required {role.required_count}: {len(eligible)} eligible users")

        # Measure ILP performance
        start_time = time.perf_counter()
        ilp_result = match_issues_to_users(issues, users, allow_partial=False, strategy="ilp")
        ilp_time = time.perf_counter() - start_time

        # Measure Backtracking performance with recursion counting
        recursion_count = [0]
        original_backtrack = globals().get('backtrack', None)

        def backtrack_wrapper(issue_idx):
            recursion_count[0] += 1
            return original_backtrack(issue_idx)

        globals()['backtrack'] = backtrack_wrapper
        start_time = time.perf_counter()
        backtrack_result = match_issues_to_users(issues, users, allow_partial=False, strategy="backtracking_basic")
        backtrack_time = time.perf_counter() - start_time
        if original_backtrack:
            globals()['backtrack'] = original_backtrack
        else:
            del globals()['backtrack']

        # Validate solutions
        ilp_valid, ilp_msg = self.validate_solution(issues, users, ilp_result)
        backtrack_valid, backtrack_msg = self.validate_solution(issues, users, backtrack_result)
        self.assertTrue(ilp_valid, f"ILP solution invalid: {ilp_msg}")
        self.assertTrue(backtrack_valid, f"Backtracking solution invalid: {backtrack_msg}")

        # Verify that solutions are non-empty (feasible)
        self.assertTrue(ilp_result, "ILP should produce a feasible solution")
        self.assertTrue(backtrack_result, "Backtracking should produce a feasible solution")

        # Verify that backtracking is faster
        self.assertLess(backtrack_time, ilp_time,
                        f"Backtracking ({backtrack_time:.4f}s) should be faster than ILP ({ilp_time:.4f}s)")

        # Log times and results for debugging
        print(f"ILP time: {ilp_time:.4f} seconds")
        print(f"Backtracking time: {backtrack_time:.4f} seconds")
        print(f"Backtracking recursions: {recursion_count[0]}")
        print(f"ILP result: {ilp_result}")
        print(f"Backtracking result: {backtrack_result}")
        print(f"ILP validation: {ilp_msg}")
        print(f"Backtracking validation: {backtrack_msg}")


if __name__ == "__main__":
    unittest.main()