
import sqlite3
from pathlib import Path

from app.database.connection import DATABASE_PATH


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "app" / "database" / "schema.sql"


def test_schema_creates_four_tables():
    assert SCHEMA_PATH.exists(), "schema.sql was not found"

    with sqlite3.connect(":memory:") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema_sql)

        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        table_names = {row[0] for row in rows}

        assert table_names == {
            "teams",
            "players",
            "matches",
            "player_stats",
        }


def test_schema_rejects_a_match_against_the_same_team():
    with sqlite3.connect(":memory:") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        cursor = connection.execute(
            "INSERT INTO teams (team_name) VALUES (?)",
            ("India",),
        )
        team_id = cursor.lastrowid

        try:
            connection.execute(
                """
                INSERT INTO matches (team1_id, team2_id)
                VALUES (?, ?)
                """,
                (team_id, team_id),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError(
                "The schema allowed a team to play against itself"
            )
