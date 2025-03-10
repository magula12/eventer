import requests
from models import initialize_data
from process import match_issues_to_users

# Same endpoint for GET and POST, but different HTTP methods
API_URL = "http://localhost:3000/eventer_api.json?key=836415703b4576d4dc5663a062a89b3a7b10055f"

def fetch_json_from_api():
    """Fetch JSON data from the Redmine plugin API (GET)."""
    try:
        response = requests.get(API_URL, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching API data: {e}")
        return None

def send_assignments_to_redmine(results):
    """
    POST the assignment results back to the same endpoint.
    We assume EventerApiController has a create_assignments action
    that handles 'assignments' in the payload.
    """
    # 'results' is something like:
    # {
    #   23: { "Režisér": [5], "Komentátor": [10] },
    #   24: { "Režisér": [1,7] },
    #   ...
    # }

    # The controller expects a structure like:
    # {
    #   "assignments": {
    #       "23": { "Režisér": [5], "Komentátor": [10] },
    #       "24": { "Režisér": [1,7] }
    #   }
    # }
    payload = { "assignments": {} }

    for issue_id, roles_dict in results.items():
        payload["assignments"][str(issue_id)] = roles_dict

    try:
        # Post to the same endpoint, but it must be configured
        # to handle POST in your routes (create_assignments action).
        response = requests.post(API_URL,
                                 json=payload,
                                 headers={"Content-Type": "application/json"})
        response.raise_for_status()
        print(f"✅ Assignments posted successfully! Status: {response.status_code}")
        print("Server response:", response.json())
    except requests.RequestException as e:
        print(f"❌ Error posting assignments: {e}")

if __name__ == "__main__":
    print("📡 Fetching data from API (GET)...")
    json_data = fetch_json_from_api()

    if json_data:
        print("✅ Data fetched successfully!")

        # Convert JSON data into Python objects (issues & users)
        issues, users = initialize_data(json_data)

        # Print loaded data for debugging
        print("\n📌 Issues Loaded:")
        for issue in issues:
            print(issue)

        print("\n📌 Users Loaded:")
        for user in users:
            print(user)

        # Run the matching algorithm
        print("\n🔄 Running Matching Algorithm with Datetime Checks...")
        results = match_issues_to_users(issues, users)

        print("\n=== FINAL RESULTS ===")
        for issue_id, role_assignments in results.items():
            print(f"Issue ID {issue_id}:")
            for role_name, assigned_ids in role_assignments.items():
                print(f"  - Role '{role_name}': {assigned_ids}")

        # Now POST results back to the same endpoint
        print("\n💾 Sending assignments to Redmine (POST)...")
        send_assignments_to_redmine(results)

    else:
        print("❌ No data fetched; exiting.")
