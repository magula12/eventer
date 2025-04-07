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

    def backtrack(idx):
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

        return backtrack(idx + 1)

    return assignment if backtrack(0) else {}


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

    def backtrack(idx):
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

        return backtrack(idx + 1)

    return assignment if backtrack(0) else {}
