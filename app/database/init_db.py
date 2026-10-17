
from app.database.connection import get_connection
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def initialize_database():
    """Create the database tables if they do not already exist."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    connection = get_connection()

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema_sql)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
