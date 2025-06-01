import json
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Issue, User
from process import match_issues_to_users
sys.setrecursionlimit(5000)  # Adjust as needed


# Load benchmark data
with open("benchmark_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

issues = [Issue(i) for i in data["issues"]]
users = [User(u) for u in data["users"]]

start = time.time()
strategy = "ilp"
results = match_issues_to_users(issues, users, strategy= strategy)
duration = time.time() - start

fully, partial, none = 0, 0, 0
for issue in issues:
    roles = results.get(issue.id, {})
    if not roles:
        none += 1
    elif all(len(roles.get(r.role, [])) == r.required_count for r in issue.required_roles):
        fully += 1
    else:
        partial += 1
print(f"🔍 Benchmarking {len(issues)} issues and {len(users)} users with strategy '{strategy}'")
print(f"✅ Benchmark complete in {duration:.2f} seconds")
print(f"✔️ Fully solved: {fully}")
print(f"⚠️ Partially solved: {partial}")
print(f"❌ Unsolved: {none}")
