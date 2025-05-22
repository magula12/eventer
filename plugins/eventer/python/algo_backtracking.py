from datetime import timedelta
from models import User, Issue

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
    best_assignment = [{}]
    best_total_rating = [0]
    current_assignment = {}
    user_schedule = {user.id: [] for user in users}
    current_rating = [0]
    recursion_count = [0]

    def is_valid(user, issue, role):
        if get_rating(user, role.role, issue.category) <= 0:
            return False

        start = issue.start_datetime
        end = issue.end_datetime or start + timedelta(hours=1)

        for od in user.off_days:
            if not (end <= od.start_datetime or start >= od.end_datetime):
                return False

        for s, e in user_schedule[user.id]:
            if is_time_overlap(s, e, start, end):
                return False

        if any(user.id in uids for uids in current_assignment.get(issue.id, {}).values()):
            return False

        return True

    def compute_max_possible_rating(issue_idx):
        max_rating = current_rating[0]
        for i in range(issue_idx, len(issues)):
            issue = issues[i]
            for role in issue.required_roles:
                available_users = [u for u in users if is_valid(u, issue, role)]
                ratings = sorted(
                    [get_rating(u, role.role, issue.category) for u in available_users],
                    reverse=True
                )[:role.required_count]
                max_rating += sum(ratings)
        return max_rating

    def backtrack(issue_idx):
        recursion_count[0] += 1
        if issue_idx == len(issues):
            if current_rating[0] > best_total_rating[0]:
                best_total_rating[0] = current_rating[0]
                best_assignment[0] = {
                    issue_id: {role: list(user_ids) for role, user_ids in roles.items()}
                    for issue_id, roles in current_assignment.items()
                }
            return
        if compute_max_possible_rating(issue_idx) <= best_total_rating[0]:
            return

        issue = issues[issue_idx]
        current_assignment[issue.id] = {}

        if assign_roles(issue, 0):
            backtrack(issue_idx + 1)
        for role in issue.required_roles:
            for user_id in current_assignment[issue.id].get(role.role, []):
                user_schedule[user_id].pop()
        del current_assignment[issue.id]

    def assign_roles(issue, role_idx):
        if role_idx == len(issue.required_roles):
            return True

        role = issue.required_roles[role_idx]
        assigned = []

        available_users = [u for u in users if is_valid(u, issue, role)]
        sorted_users = sorted(
            available_users,
            key=lambda u: get_rating(u, role.role, issue.category),
            reverse=True
        )

        if assign_users(issue, role, sorted_users, 0, assigned):
            current_assignment[issue.id][role.role] = assigned
            if assign_roles(issue, role_idx + 1):
                return True
            for user_id in assigned:
                user_schedule[user_id].pop()
            del current_assignment[issue.id][role.role]
        return False

    def assign_users(issue, role, sorted_users, user_idx, assigned):
        if len(assigned) == role.required_count:
            return True

        for i in range(user_idx, len(sorted_users)):
            user = sorted_users[i]
            assigned.append(user.id)
            end_time = issue.end_datetime or issue.start_datetime + timedelta(hours=1)
            user_schedule[user.id].append((issue.start_datetime, end_time))
            current_rating[0] += get_rating(user, role.role, issue.category)
            if assign_users(issue, role, sorted_users, i + 1, assigned):
                return True
            assigned.pop()
            user_schedule[user.id].pop()
            current_rating[0] -= get_rating(user, role.role, issue.category)
        return False

    backtrack(0)
    return best_assignment[0]