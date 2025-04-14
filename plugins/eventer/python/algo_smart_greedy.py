from datetime import timedelta
from models import User, Issue
from filter_eval import evaluate_filter_block

def smart_greedy(issues, users):
    """
    Smart greedy assignment, allowing filter violations only if no filter-passing users exist.
    Returns a dictionary: { issue_id: { role_name: [list_of_assigned_user_ids] } }
    """
    assignment = {}
    user_assignments = []  # List of (user_id, start, end) to track overlaps
    FILTER_PENALTY = 100  # Penalty for filter violations

    for issue in sorted(issues, key=lambda i: i.start_datetime):
        assignment[issue.id] = {}
        issue_end = issue.end_datetime or issue.start_datetime + timedelta(hours=3)

        for req_role in issue.required_roles:
            role = req_role.role
            count_needed = req_role.required_count
            assigned_users = []

            # Build candidates
            candidates = []
            filter_passing_candidates = []  # Track users who pass filters
            for user in users:
                # High-priority: qualifications
                if not any(q.role == role and (issue.category is None or q.category == issue.category)
                           for q in user.qualifications):
                    continue

                # High-priority: availability
                if not user.is_available(issue.start_datetime, issue_end):
                    continue

                # High-priority: overlaps
                has_conflict = any(
                    (user.id == u_id and times_overlap(issue.start_datetime, issue_end, s, e))
                    for (u_id, s, e) in user_assignments
                )
                if has_conflict:
                    continue

                # High-priority: multi-role
                already_in_issue = any(
                    user.id in users_for_role
                    for r, users_for_role in assignment[issue.id].items()
                )
                if already_in_issue:
                    continue

                # Get rating
                rating = 0
                for q in user.qualifications:
                    if q.role == role and (issue.category is None or q.category == issue.category):
                        rating = q.rating
                        break

                # Low-priority: filters
                context = {
                    "category": issue.category,
                    "start_time": issue.start_datetime,
                    "end_time": issue_end,
                    "assigned_users": []
                }
                num_filter_violations = sum(
                    1 for cf in user.custom_filters if not evaluate_filter_block(cf.conditions, context)
                )
                score = rating - num_filter_violations * FILTER_PENALTY

                # Track filter-passing users
                if num_filter_violations == 0:
                    filter_passing_candidates.append((user, score))
                candidates.append((user, score))

            # Prefer filter-passing candidates if available
            if filter_passing_candidates:
                candidates = filter_passing_candidates

            # Sort by score (descending)
            candidates.sort(key=lambda t: t[1], reverse=True)

            # Assign top candidates
            for user, _ in candidates[:count_needed]:
                assigned_users.append(user.id)
                user_assignments.append((user.id, issue.start_datetime, issue_end))

            assignment[issue.id][role] = assigned_users

    return assignment


def times_overlap(s1, e1, s2, e2):
    e1 = e1 if e1 is not None else s1 + timedelta(hours=3)
    e2 = e2 if e2 is not None else s2 + timedelta(hours=3)
    return (s1 < e2) and (s2 < e1)