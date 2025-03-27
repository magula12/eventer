from datetime import datetime
from models import User, Issue
import  algo_ILP

def match_issues_to_users(issues, users):
    #results = algo_basic.basic(issues, users)
    results = algo_ILP.ilp(issues, users)
    return results


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
