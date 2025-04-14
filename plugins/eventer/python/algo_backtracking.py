from datetime import timedelta
from models import User, Issue
from filter_eval import evaluate_filter_block


def is_time_overlap(s1, e1, s2, e2):
    e1 = e1 if e1 is not None else s1 + timedelta(hours=3)
    e2 = e2 if e2 is not None else s2 + timedelta(hours=3)
    return (s1 < e2) and (s2 < e1)


def get_rating(user, role, category):
    for q in user.qualifications:
        if q.role == role and (category is None or q.category == category):
            return q.rating
    return 0


def backtracking_basic(issues, users):
    """
    True backtracking assignment of users to issues.
    Returns a dictionary: { issue_id: { role_name: [list_of_assigned_user_ids] } }
    """
    assignment = {}
    user_schedule = {user.id: [] for user in users}

    def is_valid(user, issue, role):
        # Check qualification
        if get_rating(user, role.role, issue.category) <= 0:
            return False
        # Check time overlap with existing schedule
        end_time = issue.end_datetime or issue.start_datetime + timedelta(hours=3)
        for s, e in user_schedule[user.id]:
            if is_time_overlap(s, e, issue.start_datetime, end_time):
                return False
        # Check custom filters
        context = {
            "category": issue.category,
            "start_time": issue.start_datetime,
            "end_time": end_time,
            "assigned_users": []
        }
        if any(not evaluate_filter_block(cf.conditions, context) for cf in user.custom_filters):
            return False
        # Check if user is already assigned to another role in this issue
        if any(user.id in assigned_users for assigned_users in assignment.get(issue.id, {}).values()):
            return False
        return True

    def backtrack(idx):
        # Base case: all issues assigned
        if idx == len(issues):
            return True

        issue = issues[idx]
        assignment[issue.id] = {}

        # Try to assign all roles for this issue
        if assign_roles(issue, 0):
            # If successful, move to next issue
            if backtrack(idx + 1):
                return True
            # If next issues fail, backtrack by removing this issue's assignments
            for role in issue.required_roles:
                for user_id in assignment[issue.id].get(role.role, []):
                    user_schedule[user_id].pop()
            del assignment[issue.id]
        return False

    def assign_roles(issue, role_idx):
        # Base case: all roles assigned for this issue
        if role_idx == len(issue.required_roles):
            return True

        role = issue.required_roles[role_idx]
        assigned = []

        # Try assigning users to this role
        if assign_users(issue, role, users, 0, assigned):
            assignment[issue.id][role.role] = assigned
            # Move to next role
            if assign_roles(issue, role_idx + 1):
                return True
            # If subsequent roles fail, backtrack by undoing this role
            for user_id in assigned:
                user_schedule[user_id].pop()
            del assignment[issue.id][role.role]
        return False

    def assign_users(issue, role, users, user_idx, assigned):
        # Base case: enough users assigned for this role
        if len(assigned) == role.required_count:
            return True

        # Try each user starting from user_idx
        for i in range(user_idx, len(users)):
            user = users[i]
            if is_valid(user, issue, role):
                assigned.append(user.id)
                end_time = issue.end_datetime or issue.start_datetime + timedelta(hours=3)
                user_schedule[user.id].append((issue.start_datetime, end_time))
                # Recursively try to assign remaining users
                if assign_users(issue, role, users, i + 1, assigned):
                    return True
                # Backtrack: undo this assignment
                assigned.pop()
                user_schedule[user.id].pop()
        return False

    # Start backtracking from the first issue
    success = backtrack(0)
    return assignment if success else {}

















def backtracking_basic2(issues, users):
    assignment = {}
    user_schedule = {user.id: [] for user in users}

    def is_valid(user, issue, role):
        if get_rating(user, role.role, issue.category) <= 0:
            return False
        for s, e in user_schedule[user.id]:
            if is_time_overlap(s, e, issue.start_datetime, issue.end_datetime):
                return False
        context = {
            "category": issue.category,
            "start_time": issue.start_datetime,
            "end_time": issue.end_datetime,
            "assigned_users": []
        }
        if any(not evaluate_filter_block(cf.conditions, context) for cf in user.custom_filters):
            return False
        return True

    def backtrack2(idx):
        if idx == len(issues):
            return True
        issue = issues[idx]
        assignment[issue.id] = {}

        for role in issue.required_roles:
            assigned = []
            for user in users:
                if len(assigned) == role.required_count:
                    break
                if is_valid(user, issue, role):
                    assigned.append(user.id)
                    user_schedule[user.id].append((issue.start_datetime, issue.end_datetime))
            if len(assigned) < role.required_count:
                return False
            assignment[issue.id][role.role] = assigned

        return backtrack2(idx + 1)

    return assignment if backtrack2(0) else {}


def backtracking_heuristic(issues, users):
    assignment = {}
    user_schedule = {user.id: [] for user in users}

    def is_valid(user, issue, role):
        if get_rating(user, role.role, issue.category) <= 0:
            return False
        for s, e in user_schedule[user.id]:
            if is_time_overlap(s, e, issue.start_datetime, issue.end_datetime):
                return False
        context = {
            "category": issue.category,
            "start_time": issue.start_datetime,
            "end_time": issue.end_datetime,
            "assigned_users": []
        }
        if any(not evaluate_filter_block(cf.conditions, context) for cf in user.custom_filters):
            return False
        return True

    def order_users(role, issue):
        return sorted(
            [u for u in users if is_valid(u, issue, role)],
            key=lambda u: -get_rating(u, role.role, issue.category)
        )

    def backtrack2(idx):
        if idx == len(issues):
            return True
        issue = issues[idx]
        assignment[issue.id] = {}

        for role in sorted(issue.required_roles, key=lambda r: -r.required_count):
            assigned = []
            for user in order_users(role, issue):
                if len(assigned) == role.required_count:
                    break
                if user.id not in assigned:
                    assigned.append(user.id)
                    user_schedule[user.id].append((issue.start_datetime, issue.end_datetime))
            if len(assigned) < role.required_count:
                return False
            assignment[issue.id][role.role] = assigned

        return backtrack2(idx + 1)

    return assignment if backtrack2(0) else {}
