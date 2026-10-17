
from app.database.connection import get_connection


def seed_matches():
    """Insert a sample India vs Australia match."""
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

        required_teams = {"India", "Australia"}
        if not required_teams.issubset(team_ids):
            raise ValueError(
                "Please seed India and Australia before seeding matches."
            )

        connection.execute(
            """
            INSERT INTO matches (
                team1_id,
                team2_id,
                venue,
                match_date,
                status
            )
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM matches
                WHERE team1_id = ?
                  AND team2_id = ?
                  AND match_date = ?
            )
            """,
            (
                team_ids["India"],
                team_ids["Australia"],
                "Sample Cricket Ground",
                "2026-10-15",
                "scheduled",
                team_ids["India"],
                team_ids["Australia"],
                "2026-10-15",
            ),
        )

        connection.commit()
        print("Sample match added successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_matches()
