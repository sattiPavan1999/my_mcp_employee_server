import sqlite3


def get_test_connection():
    """Return an in-memory sqlite3 connection with the employees table created."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            role TEXT
        );
    """)
    conn.commit()
    return conn
