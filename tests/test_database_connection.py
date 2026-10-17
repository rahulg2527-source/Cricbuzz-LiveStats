
from app.database.connection import DATABASE_PATH, get_connection


def test_database_connection():
    connection = get_connection()

    try:
        cursor = connection.execute("SELECT 1")
        result = cursor.fetchone()

        assert result[0] == 1
        assert DATABASE_PATH.exists()

    finally:
        connection.close()
