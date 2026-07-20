import time

import pytest

# =====================================================================
# Mock/Stub Classes
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


# =====================================================================
# Pytest Fixtures
# =====================================================================


@pytest.fixture(scope="module")
def db_connection():
    """Runs ONCE per test module (similar to setUpClass / tearDownClass)."""
    connection = create_db_connection()
    print("\nDB connected")
    yield connection
    # Teardown runs after all tests in the module finish
    connection.close()
    print("DB disconnected")


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """Runs before and after EVERY test (similar to setUp / tearDown)."""
    cursor = db_connection.cursor()
    yield cursor
    # Teardown runs after the test completes
    cursor.close()


# =====================================================================
# Tests
# =====================================================================


def test_insert(db_cursor):
    result = db_cursor.execute("INSERT INTO users (id, name) VALUES (1, 'Alice')")
    assert result is True


def test_select(db_cursor):
    result = db_cursor.execute("SELECT * FROM users WHERE id = 1")
    assert result is True
