
from app.database.connection import get_connection


def test_real_database_has_four_tables():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        table_names = {row["name"] for row in rows}

        assert table_names == {
            "teams",
            "players",
            "matches",
            "player_stats",
        }
    finally:
        connection.close()
