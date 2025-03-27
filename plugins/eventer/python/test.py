import unittest
import sys
import os

# Ensure Python finds our module files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import User, Issue, Qualification, OffDay, RequiredRole
from process import match_issues_to_users
from helper import parse_datetime


TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")

if __name__ == "__main__":
    # Discover and run all tests in the /tests directory
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR)

    runner = unittest.TextTestRunner()
    runner.run(suite)