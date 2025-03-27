import os
import sys
import unittest
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from parent directory
from models import User, Issue
from process import match_issues_to_users

from helper import parse_datetime
from filter_eval import evaluate_filter_block


class TestFilterEvaluator(unittest.TestCase):

    def setUp(self):
        """
        Runs before each test. We can define some reusable data here.
        """
        # Example user data with one custom filter
        self.user_data = {
            "id": 1,
            "login": "admin",
            "firstname": "Redmine",
            "lastname": "Admin",
            "qualifications": [
                {"role": "Režisér", "category": "Hokej SHL", "rating": 5}
            ],
            "off_days": [],
            "custom_filters": [
                {
                    "name": "custom filter 1",
                    "conditions": {
                        "rules": {
                            "and": [
                                {
                                    ">=": [
                                        {"var": "start_time"},
                                        "18:00"
                                    ]
                                }
                            ]
                        },
                        "conditions": {
                            "and": [
                                {
                                    "==": [
                                        {"var": "category"},
                                        "EXZ"
                                    ]
                                }
                            ]
                        }
                    }
                }
            ]
        }

        # Example issue data
        self.issue_data = {
            "id": 42,
            "subject": "Basketball Game",
            "category": "EXZ",
            "category_priority": 2,
            "priority": 5,
            "start_datetime": "2025-03-17T20:30:00",
            "end_datetime": None,  # will default to 3 hours after start
            "required_roles": []
        }

    def test_simple_operator_evaluation(self):
        """
        Test a simple operator block like {"==": ["A", "A"]}.
        """
        block = {"==": ["A", "A"]}
        context = {}
        result = evaluate_filter_block(block, context)
        self.assertTrue(result, "Expected the block to evaluate to True (A == A)")

        block = {"!=": ["A", "B"]}
        result = evaluate_filter_block(block, context)
        self.assertTrue(result, "Expected (A != B) to be True")

        # Test an unsupported operator
        block = {"***": ["A", "B"]}
        with self.assertRaises(ValueError):
            evaluate_filter_block(block, context)

    def test_time_comparison(self):
        """
        Test comparing times like {">=": [{"var": "18:00"}, "start_time"]}.
        """
        block = {
            ">=": [
                {"var": "start_time"},
                "18:00"
            ]
        }

        # If start_time is 20:30, that is >= 18:00 => True
        context = {
            "start_time": datetime.datetime(2025, 3, 17, 20, 30),
        }
        result = evaluate_filter_block(block, context)
        self.assertTrue(result, "20:30 >= 18:00 should be True")

        # If start_time is 17:00 => 17:00 is NOT >= 18:00 => False
        context["start_time"] = datetime.datetime(2025, 3, 17, 17, 0)
        result = evaluate_filter_block(block, context)
        self.assertFalse(result, "17:00 >= 18:00 should be False")

    def test_in_notin(self):
        """
        Test 'in' / 'not in' operators.
        """
        block_in = {
            "in": [
                "Alice",
                {"var": "assigned_users"}
            ]
        }
        block_not_in = {
            "not in": [
                "Alice",
                {"var": "assigned_users"}
            ]
        }
        context = {
            "assigned_users": ["Alice", "Bob"]
        }

        # "Alice" in ["Alice", "Bob"] => True
        self.assertTrue(evaluate_filter_block(block_in, context))
        # "Alice" not in ["Alice", "Bob"] => False
        self.assertFalse(evaluate_filter_block(block_not_in, context))

    def test_custom_filter_evaluation(self):
        """
        Test the entire CustomFilter -> evaluate_for_issue logic
        using the data in setUp.
        """
        user = User(self.user_data)
        issue = Issue(self.issue_data)

        # There's exactly 1 custom filter: "custom filter 1"
        cf = user.custom_filters[0]

        # Evaluate the filter. With the default issue start_time=20:30, category=EXZ:
        # 1) rules => 18:00 <= start_time => True
        # 2) conditions => "EXZ" == category => True
        # => combined => True
        result = cf.evaluate_for_issue(issue)
        self.assertTrue(result, "Expecting True when category=EXZ and start_time=20:30")

        # If we change the category or start_time, we can test negative cases
        issue.category = "XYZ"  # Not EXZ => conditions block fails
        result = cf.evaluate_for_issue(issue)
        self.assertFalse(result, "Expecting False if category != EXZ")
        issue.category = "EXZ"  # revert

        # Now change start_time to 17:00 => rules block fails
        issue.start_datetime = parse_datetime("2025-03-17T17:00:00")
        result = cf.evaluate_for_issue(issue)
        self.assertFalse(result, "Expecting False if start_time < 18:00")

    def test_and_or_blocks(self):
        """
        Test nested 'and', 'or' blocks in evaluate_filter_block.
        """
        # (category == EXZ) OR (category == ABC)
        block = {
            "or": [
                { "==": [ {"var": "category"}, "EXZ" ] },
                { "==": [ {"var": "category"}, "ABC" ] }
            ]
        }
        context = {"category": "EXZ"}
        self.assertTrue(evaluate_filter_block(block, context), "EXZ matches the first or condition")

        context["category"] = "ABC"
        self.assertTrue(evaluate_filter_block(block, context), "ABC matches the second or condition")

        context["category"] = "XYZ"
        self.assertFalse(evaluate_filter_block(block, context), "XYZ fails both conditions in the 'or'")

        # (category == EXZ) AND (start_time >= 18:00)
        block = {
            "and": [
                { "==": [ {"var": "category"}, "EXZ" ] },
                { ">=": [ {"var": "start_time"}, "18:00" ] }
            ]
        }
        context = {
            "category": "EXZ",
            "start_time": datetime.datetime(2025, 3, 17, 19, 0)
        }
        self.assertTrue(evaluate_filter_block(block, context), "Both conditions are True")

        context["category"] = "XYZ"
        self.assertFalse(evaluate_filter_block(block, context), "First condition fails")


if __name__ == "__main__":
    unittest.main()
