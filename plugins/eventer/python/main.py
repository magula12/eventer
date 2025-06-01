from flask import Flask, request, jsonify
import requests
from models import initialize_data
from process import match_issues_to_users
import io
import sys

app = Flask(__name__)

# Same endpoint & key as before
API_URL = "http://redmine:3000/eventer_api.json?key=836415703b4576d4dc5663a062a89b3a7b10055f"

def send_assignments_to_redmine(results):
    """
    POST the assignment results back to the same endpoint,
    using the same structure you had before.
    e.g. { 'assignments': { '23': { 'Režisér': [5], ... }, ... } }
    """
    payload = { "assignments": {} }
    for issue_id, roles_dict in results.items():
        # Convert integer keys to strings
        payload["assignments"][str(issue_id)] = roles_dict

    try:
        response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        print(f"✅ Assignments posted successfully! Status: {response.status_code}")
        print("Server response:", response.json())
    except requests.RequestException as e:
        print(f"❌ Error posting assignments: {e}")

@app.route("/run_algorithm", methods=["POST"])
def run_algorithm():

    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        print()
        allow_partial = request.json.get("partial_solution", False)
        print(f"ℹ️ Partial solution allowed: {allow_partial}")
        
        # Get data directly from the POST request
        json_data = request.json.get("data")
        if not json_data:
            print("❌ No data received in request.")
            return jsonify({"status": "error", "output": mystdout.getvalue()}), 400

        print("✅ Data received successfully!\n")

        #print(json_data)
        issues, users = initialize_data(json_data)

        print("📌 Issues Loaded:")
        for issue in issues:
            print(str(issue))

        print("\n📌 Users Loaded:")
        for user in users:
            print(str(user))

        print("\n🔄 Running Matching Algorithm with Datetime Checks...")
        results = match_issues_to_users(issues, users, allow_partial)

        print("\n=== FINAL RESULTS ===")
        for issue_id, role_assignments in results.items():
            print(f"Issue ID {issue_id}:")
            for role_name, user_ids in role_assignments.items():
                print(f"  - Role '{role_name}': {user_ids}")

        print("\n💾 Sending assignments to Redmine...")
        send_assignments_to_redmine(results)

        # Restore stdout
        sys.stdout = old_stdout

        return jsonify({
            "status": "success",
            "output": mystdout.getvalue()
        }), 200

    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({
            "status": "error",
            "output": mystdout.getvalue() + f"\n❌ Exception occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    # Make sure to listen on 0.0.0.0 so Redmine can reach us
    app.run(host="0.0.0.0", port=5000)