# plugins/eventer/python/test.py

import sys
import os

# Ensure Python finds our module files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all necessary components
from models import User, Issue, Qualification, OffDay, RequiredRole
from process import match_issues_to_users
from helper import parse_datetime

print("🚀 Test Environment Ready! You can now manually run any functions.")

# Example Usage (You can modify this part to test different things)
if __name__ == "__main__":
    print("\n📌 Example: Parsing datetime")
    dt = parse_datetime("2025-03-10T13:20:00Z")
    print("Parsed Datetime:", dt)

    print("\n📌 Example: Creating a User")
    user_data = {
        "id": 1,
        "login": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "qualifications": [{"role": "Režisér", "category": "Hokej SHL", "rating": 9}],
        "off_days": [{"start_datetime": "2025-03-10T09:00:00", "end_datetime": "2025-03-10T13:00:00"}]
    }
    user = User(user_data)
    print(user)

    print("\n📌 Example: Checking Availability")
    start_time = parse_datetime("2025-03-10T10:00:00")
    end_time = parse_datetime("2025-03-10T12:00:00")
    print(f"User Available from {start_time} to {end_time}: {user.is_available(start_time, end_time)}")

    print("\n📌 Example: Creating an Issue")
    issue_data = {
        "id": 99,
        "subject": "Test Issue",
        "start_datetime": "2025-03-07T10:00:00",
        "end_datetime": None,
        "category": "Hokej SHL",
        "category_priority": None,
        "priority": "Normálna",
        "required_roles": [
            {"role": "Režisér", "required_count": 1, "assigned_users": []}
        ]
    }
    issue = Issue(issue_data)
    print(issue)

    print("\n✅ All Imports & Basic Tests Loaded Successfully! You can now manually call functions.")
