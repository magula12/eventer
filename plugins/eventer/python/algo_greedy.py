from datetime import timedelta
from models import User, Issue
from filter_eval import evaluate_filter_block


def greedy(issues, users):
    """
    Greedy assignment of users to issues with constraint checking.
    Returns a dictionary: { issue_id: { role_name: [list_of_assigned_user_ids] } }
    """
    assignment = {}
    user_assignments = []

    for issue in sorted(issues, key=lambda i: i.start_datetime):
        assignment[issue.id] = {}
        issue_end = issue.end_datetime or issue.start_datetime + timedelta(hours=3)

        for req_role in issue.required_roles:
            role = req_role.role
            count_needed = req_role.required_count
            assigned_users = []

            # Handle forward assignments
            forward_assigned = [u.id for u in req_role.assigned_users]
            for user_id in forward_assigned:
                assigned_users.append(user_id)
                user_assignments.append((user_id, issue.start_datetime, issue_end))

            # If we still need more users, look for additional candidates
            if len(assigned_users) < count_needed:
                candidates = []
                for user in users:
                    if user.id in assigned_users:
                        continue

                    if any(q.role == role and (issue.category is None or q.category == issue.category)
                           for q in user.qualifications):

                        if not user.is_available(issue.start_datetime, issue_end):
                            continue

                        has_conflict = any(
                            (user.id == u_id and times_overlap(issue.start_datetime, issue_end, s, e))
                            for (u_id, s, e) in user_assignments
                        )
                        if has_conflict:
                            continue

                        context = {
                            "category": issue.category,
                            "start_time": issue.start_datetime,
                            "end_time": issue_end,
                            "assigned_users": []
                        }
                        if any(not evaluate_filter_block(cf.conditions, context) for cf in user.custom_filters):
                            continue

                        already_in_issue = any(
                            user.id in users_for_role
                            for r, users_for_role in assignment[issue.id].items()
                        )
                        if already_in_issue:
                            continue

                        rating = 0
                        for q in user.qualifications:
                            if q.role == role and (issue.category is None or q.category == issue.category):
                                rating = q.rating
                                break

                        candidates.append((user, rating))

                # Sort candidates by rating (descending)
                candidates.sort(key=lambda t: t[1], reverse=True)

                # Assign remaining needed users
                remaining_needed = count_needed - len(assigned_users)
                for user, _ in candidates[:remaining_needed]:
                    assigned_users.append(user.id)
                    user_assignments.append((user.id, issue.start_datetime, issue_end))

            assignment[issue.id][role] = assigned_users

    return assignment


def times_overlap(s1, e1, s2, e2):
    e1 = e1 if e1 is not None else s1 + timedelta(hours=3)
    e2 = e2 if e2 is not None else s2 + timedelta(hours=3)
    return (s1 < e2) and (s2 < e1)