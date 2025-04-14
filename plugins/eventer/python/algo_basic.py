from plugins.eventer.python.process import is_qualified_for_role, is_time_overlap


def basic(issues, users):
    """
        Attempt to assign users to issues based on:
          1. Pre-existing assignments
          2. Role qualifications (role + category if needed)
          3. Off-days (user.is_available)
          4. Check for overlapping assignments (no double-booking)
          5. Provide partial solutions if not enough candidates
          6. Placeholder for custom filters (commented out)
        """
    results = {}

    # We'll keep a record of who is assigned to which timeframe:
    # assigned_schedule = {user_id: list of (start, end, issue_id)}
    assigned_schedule = {u.id: [] for u in users}

    print("\n==== Start Matching Algorithm with Datetime Checks ====")

    for issue in issues:
        print(f"\n=== Matching for Issue: {issue.subject} (ID={issue.id}) ===")
        # Prepare a sub-dict for this issue in results
        results[issue.id] = {}

        for req_role in issue.required_roles:
            role_name = req_role.role
            required_count = req_role.required_count
            assigned_list = []

            # 1) Keep existing assigned users
            for assigned_user in req_role.assigned_users:
                assigned_list.append(assigned_user.id)

            if len(assigned_list) >= required_count:
                print(f"  - {role_name} already fulfilled by existing assignment(s).")
                results[issue.id][role_name] = assigned_list
                # Mark schedule for assigned users
                for uid in assigned_list:
                    assigned_schedule[uid].append((issue.start_datetime, issue.end_datetime, issue.id))
                continue

            needed = required_count - len(assigned_list)
            print(f"  - Need {needed} more user(s) for role '{role_name}'.")

            # 2) Gather qualified + available candidates
            # Check role, category, off-days, and no overlap with existing assigned schedule
            candidates = []
            for user in users:
                if user.id in assigned_list:
                    continue  # already assigned

                # Check if user is qualified
                if not is_qualified_for_role(user, role_name, issue.category):
                    continue

                # Check off-days
                if not user.is_available(issue.start_datetime, issue.end_datetime):
                    continue

                # Check schedule overlap
                if any(is_time_overlap(issue.start_datetime, issue.end_datetime, s[0], s[1])
                       for s in assigned_schedule[user.id]):
                    # The user is assigned to another issue that overlaps
                    continue

                # (Optional) Evaluate custom filters:
                # if not passes_custom_filters(user, issue):
                #     continue

                candidates.append(user)

            # 3) Assign as many as we can
            if len(candidates) >= needed:
                # Sort candidates by rating in descending order before choosing
                candidates.sort(key=lambda u: u.get_role_rating(role_name, issue.category), reverse=True)

                # Fill the role with the best candidates
                chosen = candidates[:needed]
                assigned_list.extend([u.id for u in chosen])

                # Add schedule
                for u in chosen:
                    assigned_schedule[u.id].append((issue.start_datetime, issue.end_datetime, issue.id))

                print(f"    + Assigned: {[f'{u.firstname} {u.lastname}' for u in chosen]}")
            else:
                # Partial fill if we have some candidates
                if candidates:
                    assigned_list.extend([u.id for u in candidates])
                    for u in candidates:
                        assigned_schedule[u.id].append((issue.start_datetime, issue.end_datetime, issue.id))
                    print(f"    + Partially assigned: {[f'{u.firstname} {u.lastname}' for u in candidates]}")
                    still_missing = needed - len(candidates)
                    print(f"    ❌ Still missing {still_missing} user(s) for '{role_name}'.")
                else:
                    print(f"    ❌ No qualified or available users for '{role_name}'.")

            results[issue.id][role_name] = assigned_list

    return results

from plugins.eventer.python.process import is_qualified_for_role

def very_basic(issues, users):
    """
    Very basic assignment of users to issues using simple loops.
    Only checks:
      1. Role qualifications (role + category if needed)
      2. Basic availability (off-days via user.is_available)
    No overlaps, no ratings, no pre-existing assignments, no partial solutions.
    """
    results = {}

    print("\n==== Very Basic Matching Algorithm ====")

    for issue in issues:
        print(f"\n=== Matching for Issue: {issue.subject} (ID={issue.id}) ===")
        results[issue.id] = {}

        for req_role in issue.required_roles:
            role_name = req_role.role
            required_count = req_role.required_count
            assigned_list = []

            print(f"  - Assigning {required_count} user(s) for role '{role_name}'.")

            # Loop through users and assign the first qualified and available ones
            for user in users:
                if len(assigned_list) == required_count:
                    break  # Stop once we have enough

                # Check if user is qualified
                if not is_qualified_for_role(user, role_name, issue.category):
                    continue

                # Check basic availability (off-days)
                if not user.is_available(issue.start_datetime, issue.end_datetime):
                    continue

                # Assign the user
                assigned_list.append(user.id)
                print(f"    + Assigned: {user.firstname} {user.lastname}")

            results[issue.id][role_name] = assigned_list
            if len(assigned_list) < required_count:
                print(f"    ❌ Failed to assign enough users for '{role_name}' (got {len(assigned_list)} of {required_count}).")

    return results
