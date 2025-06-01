from datetime import datetime
from models import User, Issue
import  algo_ILP, algo_greedy, algo_backtracking, algo_smart_greedy

def match_issues_to_users(issues, users, allow_partial=False, strategy="ilp"):
    if strategy == "greedy":
        return algo_greedy.greedy(issues, users)
    elif strategy == "backtracking_basic":
        return algo_backtracking.backtracking_basic(issues, users)
    elif strategy == "smart_greedy":
        return algo_smart_greedy.smart_greedy(issues, users)
    else:
        return algo_ILP.ilp(issues, users, allow_partial,filter_penalty=0)

def is_qualified_for_role(user, role, category):
    for q in user.qualifications:
        if q.role == role and (category is None or q.category == category):
            return True
    return False

def is_time_overlap(s1, e1, s2, e2):
    if e1 is None:
        e1 = s1
    if e2 is None:
        e2 = s2

    return (s1 < e2) and (s2 < e1)
