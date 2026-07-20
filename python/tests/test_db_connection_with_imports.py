import unittest
import sys
import os

# Append the python directory to sys.path so we can import from concepts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =====================================================================
# WAY 2: Importing Classes from an External Module
# =====================================================================
from concepts.db_connection import create_db_connection


class TestDatabaseWithImports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Runs ONCE — setup database connection
        cls.connection = create_db_connection()
        print("DB connected (external module)")

    def setUp(self):
        # Runs before EVERY test
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.close()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        print("DB disconnected (external module)")

    def test_insert(self):
        result = self.cursor.execute("INSERT INTO users (id, name) VALUES (1, 'Alice')")
        self.assertTrue(result)

    def test_select(self):
        result = self.cursor.execute("SELECT * FROM users WHERE id = 1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
