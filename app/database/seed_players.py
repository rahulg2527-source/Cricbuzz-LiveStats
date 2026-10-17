
from app.database.connection import get_connection


def seed_players():
    """Insert sample players linked to their teams."""
    connection = get_connection()

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        teams = connection.execute(
            "SELECT team_id, team_name FROM teams"
        ).fetchall()

        team_ids = {
            row["team_name"]: row["team_id"]
            for row in teams
        }

        players = [
            ("Sample India Batter", "Batter", team_ids["India"]),
            ("Sample Australia Bowler", "Bowler", team_ids["Australia"]),
        ]

        connection.executemany(
            """
            INSERT INTO players (player_name, role, team_id)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM players
                WHERE player_name = ? AND team_id = ?
            )
            """,
            [
                (name, role, team_id, name, team_id)
                for name, role, team_id in players
            ],
        )

        connection.commit()
        print("Sample players added successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_players()
