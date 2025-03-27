from datetime import datetime, timedelta
from typing import List, Dict, Any
from helper import parse_datetime
from filter_eval import evaluate_filter_block

class Qualification:
    def __init__(self, role: str, category: str, rating: int):
        self.role = role
        self.category = category
        self.rating = rating

    def __repr__(self):
        return f"{self.role} ({self.category}) - Rating: {self.rating}"


class OffDay:
    def __init__(self, start_datetime: str, end_datetime: str):
        self.start_datetime = parse_datetime(start_datetime)
        self.end_datetime = parse_datetime(end_datetime)

    def __repr__(self):
        return f"OffDay({self.start_datetime} to {self.end_datetime})"

    def conflicts_with(self, start, end):
            if end is None:
                # If the event has no end, treat it as an instant or indefinite
                return (self.start_datetime <= start <= self.end_datetime)
            # overlap check
            return not (self.end_datetime < start or self.start_datetime > end)


class CustomFilter:
    def __init__(self, name: str, conditions: Dict[str, Any]):
        self.name = name
        self.conditions = conditions  # e.g. { "rules": {...}, "conditions": {...} }

    def __repr__(self):
        return f"<Filter: {self.name}>"

    def evaluate_for_issue(self, issue: "Issue") -> bool:
        context = {
            "category": issue.category,
            "start_time": issue.start_datetime,
            "end_time": issue.end_datetime,
            "assigned_users": [u.firstname for r in issue.required_roles for u in r.assigned_users],
            "name": issue.subject,
        }

        rules_block = self.conditions.get("rules")
        rules_result = True
        if rules_block:
            rules_result = evaluate_filter_block(rules_block, context)

        conditions_block = self.conditions.get("conditions")
        conditions_result = True
        if conditions_block:
            conditions_result = evaluate_filter_block(conditions_block, context)

        return rules_result and conditions_result


class User:
    def __init__(self, user_data: Dict):
        self.id = user_data["id"]
        self.login = user_data.get("login", "")
        self.firstname = user_data["firstname"]
        self.lastname = user_data["lastname"]
        # Build qualifications
        self.qualifications = [
            Qualification(**q) for q in user_data.get("qualifications", [])
        ]
        # Build off-days
        self.off_days = [OffDay(**od) for od in user_data.get("off_days", [])]
        # Build custom filters
        self.custom_filters = [CustomFilter(**cf) for cf in user_data.get("custom_filters", [])]


    def __repr__(self):
        return f"User: {self.firstname} {self.lastname} ({self.login})"

    def is_available(self, start: datetime, end: datetime) -> bool:
        """
        True if user is NOT on off-day for this timeframe.
        This doesn't check assignment conflicts (issue overlap).
        """
        for off_day in self.off_days:
            if off_day.conflicts_with(start, end):
                return False
        return True

    def get_role_rating(self, role: str, category: str) -> int:
        """
        Returns the user's rating for a given role in a specific category.
        If the user is not qualified for the role in that category, returns 0.
        """
        for qualification in self.qualifications:
            if qualification.role == role and qualification.category == category:
                return qualification.rating
        return 0  # If the user is not qualified, return 0



class RequiredRole:
    def __init__(self, role: str, required_count: int, assigned_users: List[Dict]):
        self.role = role
        self.required_count = required_count
        # Each assigned_user is partial data. We'll adapt it to full 'User' if possible.
        self.assigned_users = [User(u) for u in assigned_users]

    def __repr__(self):
        return f"<RequiredRole: {self.role} needs {self.required_count}, assigned: {len(self.assigned_users)}>"


class Issue:
    def __init__(self, issue_data):
        self.id = issue_data["id"]
        self.subject = issue_data["subject"]
        self.category = issue_data["category"]
        self.category_priority = issue_data["category_priority"]
        self.priority = issue_data["priority"]

        # Use your custom parse_datetime function for start_datetime
        self.start_datetime = parse_datetime(issue_data["start_datetime"])
        if self.start_datetime is None:
            raise ValueError("start_datetime is required and could not be parsed.")

        end_str = issue_data.get("end_datetime")
        parsed_end = parse_datetime(end_str) if end_str else None
        self.end_datetime = parsed_end if parsed_end is not None else self.start_datetime + timedelta(hours=3)

        self.required_roles = [
            RequiredRole(**rr) for rr in issue_data.get("required_roles", [])
        ]

    def __repr__(self):
        cat = self.category if self.category else "None"
        return f"Issue: {self.subject} ({cat}, Priority: {self.priority})"


def initialize_data(json_data):
    """Create lists of Issue and User objects from JSON."""
    issues = [Issue(i) for i in json_data["issues"]]
    users = [User(u) for u in json_data["users"]]
    return issues, users
