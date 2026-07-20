import time


class Cursor:
    def __init__(self):
        self.is_closed = False

    def execute(self, query: str, params=None):
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
    time.sleep(0.1)  # Simulate expensive database connection setup
    return DatabaseConnection()
