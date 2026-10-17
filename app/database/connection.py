
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "cricbuzz.db"


def get_connection():
    """Create a database connection with foreign-key enforcement enabled."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign-key enforcement for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    # Return rows that can be accessed by column name.
    connection.row_factory = sqlite3.Row

    return connection
