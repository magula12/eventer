from datetime import datetime
from models import User, Issue
import  algo_ILP, algo_greedy, algo_backtracking

def match_issues_to_users(issues, users, allow_partial=False, strategy="ilp"):
    if strategy == "greedy":
        return algo_greedy.greedy(issues, users)
    elif strategy == "backtracking_basic":
        return algo_backtracking.backtracking_basic(issues, users)
    elif strategy == "backtracking_heuristic":
        return algo_backtracking.backtracking_heuristic(issues, users)
    else:
        return algo_ILP.ilp(issues, users, allow_partial)


def is_qualified_for_role(user, role, category):
    """Check if user has a qualification matching role & category (or if category is None)."""
    for q in user.qualifications:
        # If issue.category is None, we skip category check
        if q.role == role and (category is None or q.category == category):
            return True
    return False


def is_time_overlap(s1, e1, s2, e2):
    """Return True if timeframes (s1,e1) and (s2,e2) overlap."""
    # If one event is open-ended (end=None), treat as indefinite from start
    if e1 is None:
        e1 = s1  # treat as instant or indefinite
    if e2 is None:
        e2 = s2

    # Overlap if start1 < end2 and start2 < end1
    return (s1 < e2) and (s2 < e1)


# Placeholder for custom filters (commented out)
def passes_custom_filters(user, issue):
    # For each custom filter in user.custom_filters:
    #   if not evaluate_filter(cf, issue):
    #       return False
    return True
