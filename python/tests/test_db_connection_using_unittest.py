import unittest
import time

# =====================================================================
# WAY 1: Inline Mock/Stub Classes (Self-contained within the test file)
# =====================================================================


class Cursor:
    def __init__(self):
        self.is_closed = False

    def execute(self, query: str):
        if self.is_closed:
            raise RuntimeError("Cannot execute query on a closed cursor")
        print(f"SQL Executing: {query}")
        return True

    def close(self):
        self.is_closed = True
        print("Cursor closed")


class DatabaseConnection:
    def __init__(self):
        self.is_closed = False

    def cursor(self):
        if self.is_closed:
            raise RuntimeError("Cannot open cursor on a closed connection")
        return Cursor()

    def close(self):
        self.is_closed = True
        print("Connection closed")


def create_db_connection():
    print("Connecting to database...")
    time.sleep(0.1)  # Simulate network latency/setup overhead
    return DatabaseConnection()


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Runs ONCE — expensive setup here
        cls.connection = create_db_connection()  # takes 2 seconds
        print("DB connected")

    def setUp(self):
        # Runs before EVERY test — cheap setup here
        self.cursor = self.connection.cursor()  # fast, new cursor each time

    def tearDown(self):
        self.cursor.close()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        print("DB disconnected")

    def test_insert(self):  # setUpClass already ran; setUp runs now
        result = self.cursor.execute("INSERT INTO users (id, name) VALUES (1, 'Alice')")
        self.assertTrue(result)

    def test_select(self):  # setUp runs again; setUpClass does NOT
        result = self.cursor.execute("SELECT * FROM users WHERE id = 1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
