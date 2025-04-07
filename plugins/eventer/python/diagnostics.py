from filter_eval import evaluate_filter_block


def diagnose(issues, users):
    print("🔍 Diagnosing infeasibility...\n")

    # 1) Local check: For each issue, see how many matching users each role has
    for issue in issues:
        for role_req in issue.required_roles:
            role = role_req.role
            needed = role_req.required_count

            matching_users = []
            for user in users:
                # Check qualifications
                if not any(q.role == role and (issue.category is None or q.category == issue.category)
                           for q in user.qualifications):
                    continue

                # Check availability
                if not user.is_available(issue.start_datetime, issue.end_datetime):
                    continue

                # Check custom filters
                context = {
                    "category": issue.category,
                    "start_time": issue.start_datetime,
                    "end_time": issue.end_datetime,
                    "assigned_users": []
                }
                if any(not evaluate_filter_block(cf.conditions, context) for cf in user.custom_filters):
                    continue

                matching_users.append(user)

            print(f"Issue {issue.id} '{issue.subject}' | Role '{role}' → Needed: {needed}, Available: {len(matching_users)}")
            # You could uncomment to see details:
            for mu in matching_users:
                print(f"    ✅ {mu.id} - {mu.firstname} {mu.lastname}")

    # 2) Global check: Pairwise overlap conflict
    # For any pair of overlapping issues, see if there's enough distinct users to fill *all* roles
    conflicts = detect_pairwise_conflicts(issues, users)
    if conflicts:
        print("\n🔎 Potential Overlap Conflicts:")
        for c in conflicts:
            print(f"⚠️ {c}")
    else:
        print("\nNo direct overlap conflict found via pairwise check. Possibly a more complex chain overlap, or ILP constraints are stricter.")

def detect_pairwise_conflicts(issues, users):
    """
    For each pair of issues that overlap in time, see if the sum of all roles needed
    can be filled by enough *distinct* users. If not, it's a global conflict.
    """
    conflicts = []
    # Sort issues by start time for easier reading
    sorted_issues = sorted(issues, key=lambda i: i.start_datetime)

    for i1_index in range(len(sorted_issues)):
        for i2_index in range(i1_index + 1, len(sorted_issues)):
            i1 = sorted_issues[i1_index]
            i2 = sorted_issues[i2_index]

            # Check if times overlap
            if not times_overlap(i1.start_datetime, i1.end_datetime, i2.start_datetime, i2.end_datetime):
                continue

            # Gather all roles needed for i1 and i2
            needed_slots = []
            for issue in (i1, i2):
                for r_req in issue.required_roles:
                    needed_slots.append({
                        "issue_id": issue.id,
                        "role_name": r_req.role,
                        "count": r_req.required_count,
                        "candidates": find_candidates(users, issue, r_req.role)
                    })

            total_needed = sum(slot["count"] for slot in needed_slots)
            # Flatten all candidate user IDs
            all_candidates = set()
            for slot in needed_slots:
                for u in slot["candidates"]:
                    all_candidates.add(u.id)

            if len(all_candidates) < total_needed:
                msg = (f"Issues {i1.id} '{i1.subject}' and {i2.id} '{i2.subject}' overlap, "
                       f"combined roles need {total_needed} user(s), "
                       f"but only {len(all_candidates)} distinct candidate(s) can fill them.")
                conflicts.append(msg)

    return conflicts

# Helper to see if times overlap
def times_overlap(s1, e1, s2, e2):
    return (s1 < e2) and (s2 < e1)

# Helper to find the list of candidate users for a single role in a single issue
def find_candidates(users, issue, role):
    from datetime import datetime
    cands = []
    for user in users:
        # If user qualifies for the role
        if any(q.role == role and (issue.category is None or q.category == issue.category)
               for q in user.qualifications):
            # If user is available
            if user.is_available(issue.start_datetime, issue.end_datetime):
                # If user passes custom filters
                ctx = {
                    "category": issue.category,
                    "start_time": issue.start_datetime,
                    "end_time": issue.end_datetime,
                    "assigned_users": []
                }
                if not any(not evaluate_filter_block(cf.conditions, ctx) for cf in user.custom_filters):
                    cands.append(user)
    return cands
