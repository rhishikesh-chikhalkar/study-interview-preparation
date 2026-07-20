import os
import sys

import pytest

# Append the python directory to sys.path so we can import from concepts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from concepts.db_connection import create_db_connection

# =====================================================================
# Pytest Fixtures
# =====================================================================


@pytest.fixture(scope="module")
def db_connection():
    """Runs ONCE per test module."""
    connection = create_db_connection()
    print("\nDB connected (external module)")
    yield connection
    connection.close()
    print("DB disconnected (external module)")


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """Runs before and after EVERY test."""
    cursor = db_connection.cursor()
    yield cursor
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
