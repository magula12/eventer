import pulp
from datetime import timedelta
from models import User, Issue
from filter_eval import evaluate_filter_block  # Import filter evaluation
import algo_greedy
import diagnostics

def ilp(issues, users, allow_partial = False):
    """
    ILP-based assignment of users to issues with custom filtering.
    Returns a dictionary: { issue_id: { role_name: [list_of_assigned_user_ids] } }
    """
    # Ensure every issue has an end_datetime: default to start_datetime + 3 hours if None.
    for issue in issues:
        if issue.end_datetime is None:
            issue.end_datetime = issue.start_datetime + timedelta(hours=3)

    # Build a list of issue-role combinations with details.
    issue_roles = []
    for issue in issues:
        for req_role in issue.required_roles:
            issue_roles.append({
                "issue_id": issue.id,
                "subject": issue.subject,
                "role": req_role.role,
                "required_count": req_role.required_count,
                "start": issue.start_datetime,
                "end": issue.end_datetime,
                "category": issue.category
            })

    # Build lookup for issue time windows (for overlap constraints)
    issue_time = {issue.id: (issue.start_datetime, issue.end_datetime) for issue in issues}

    # Create the ILP model.
    model = pulp.LpProblem("Issue_Assignment", pulp.LpMaximize)
    x = {}  # Decision variables: keys (issue_id, user_id, role) -> binary variable

    # Helper function: returns user's rating for (role, category) or 0 if unqualified.
    def get_rating(user, role, category):
        for q in user.qualifications:
            if q.role == role and (category is None or q.category == category):
                return q.rating
        return 0

    # Create decision variables only if the user is qualified, available, and passes custom filters.
    for ir in issue_roles:
        i_id = ir["issue_id"]
        role = ir["role"]
        cat = ir["category"]
        for user in users:
            rating = get_rating(user, role, cat)
            if rating <= 0:
                continue  # User not qualified

            if not user.is_available(ir["start"], ir["end"]):
                continue  # User not available

            # 🚀 **Check if the user passes their custom filters for this issue**
            issue_context = {
                "category": ir["category"],
                "start_time": ir["start"],
                "end_time": ir["end"],
                "assigned_users": []  # We can extend this if needed
            }

            # If any of the user's filters return `False`, skip the user
            if any(not evaluate_filter_block(cf.conditions, issue_context) for cf in user.custom_filters):
                continue  # User fails filter

            var_name = f"x_{i_id}_{user.id}_{role}"
            x[(i_id, user.id, role)] = pulp.LpVariable(var_name, cat=pulp.LpBinary)

    # Objective: maximize the total rating of assignments.
    model += pulp.lpSum(
        get_rating(u, ir["role"], ir["category"]) * x[(ir["issue_id"], u.id, ir["role"])]
        for ir in issue_roles
        for u in users if (ir["issue_id"], u.id, ir["role"]) in x
    ), "Total_Rating"

    # Constraint 1: For each issue-role, assign exactly the required number of users.
    for ir in issue_roles:
        i_id = ir["issue_id"]
        role = ir["role"]
        req_count = ir["required_count"]
        vars_for_ir = [x[(i_id, u.id, role)] for u in users if (i_id, u.id, role) in x]
        if not vars_for_ir:
            print(f"⚠️ No available users for issue {i_id}, role '{role}' — Debug")
        model += pulp.lpSum(vars_for_ir) == req_count, f"ReqCount_{i_id}_{role}"

    # Constraint: Prevent same user assigned to multiple roles within one issue
    for issue in issues:
        for user in users:
            vars_same_issue = [
                x[(issue.id, user.id, role.role)]
                for role in issue.required_roles
                if (issue.id, user.id, role.role) in x
            ]
            if vars_same_issue:
                model += pulp.lpSum(vars_same_issue) <= 1, f"NoMultiRole_{issue.id}_{user.id}"

    # Helper: Check if two time periods overlap.
    def times_overlap(s1, e1, s2, e2):
        e1 = e1 if e1 is not None else s1 + timedelta(hours=3)
        e2 = e2 if e2 is not None else s2 + timedelta(hours=3)
        return (s1 < e2) and (s2 < e1)

    # Constraint 2: A user cannot be double-booked for overlapping issues.
    for u in users:
        for i1 in issues:
            for i2 in issues:
                if i1.id >= i2.id:
                    continue
                (s1, e1) = issue_time[i1.id]
                (s2, e2) = issue_time[i2.id]
                if times_overlap(s1, e1, s2, e2):
                    vars_i1 = [x[(i1.id, u.id, req.role)]
                               for req in i1.required_roles if (i1.id, u.id, req.role) in x]
                    vars_i2 = [x[(i2.id, u.id, req.role)]
                               for req in i2.required_roles if (i2.id, u.id, req.role) in x]
                    if vars_i1 or vars_i2:
                        model += pulp.lpSum(vars_i1 + vars_i2) <= 1, f"NoDouble_{u.id}_{i1.id}_{i2.id}"

    # Solve the model.
    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)
    if pulp.LpStatus[model.status] != "Optimal":
        print("Warning: ILP did not reach an optimal solution. Status:", pulp.LpStatus[model.status])
        with open("infeasible_model.lp", "w", encoding="utf-8") as f:
            f.write(str(model))
        diagnostics.diagnose(issues, users)  # 🧠 Diagnostic trigger

        if allow_partial:
            print("🔍 Returning partial assignment...")
            return algo_greedy.greedy(issues, users)
        return {}  # No solution found

    # Parse the solution.
    assignment = {}
    for ir in issue_roles:
        i_id = ir["issue_id"]
        role = ir["role"]
        if i_id not in assignment:
            assignment[i_id] = {}
        if role not in assignment[i_id]:
            assignment[i_id][role] = []
        for u in users:
            key = (i_id, u.id, role)
            if key in x and pulp.value(x[key]) == 1:
                assignment[i_id][role].append(u.id)

    # Ensure all issues exist in the assignment dictionary.
    for issue in issues:
        if issue.id not in assignment:
            assignment[issue.id] = {}
    return assignment

# Example usage:
if __name__ == "__main__":
    # Load issues and users (this is just a placeholder)
    issues = []  # Your list of Issue objects
    users = []  # Your list of User objects
    result = ilp(issues, users, allow_partial = False)
    print("Assignment:", result)
