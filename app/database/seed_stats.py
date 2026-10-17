
from app.database.connection import get_connection


def seed_player_stats():
    """Insert sample player performances for the sample match."""
    connection = get_connection()

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        rows = connection.execute(
            """
            SELECT p.player_id, p.player_name, m.match_id
            FROM players AS p
            CROSS JOIN matches AS m
            JOIN teams AS t ON p.team_id = t.team_id
            WHERE m.match_date = '2026-10-15'
              AND m.venue = 'Sample Cricket Ground'
              AND (
                  (p.player_name = 'Sample India Batter'
                   AND t.team_name = 'India')
                  OR
                  (p.player_name = 'Sample Australia Bowler'
                   AND t.team_name = 'Australia')
              )
            """
        ).fetchall()

        player_ids = {
            row["player_name"]: (row["player_id"], row["match_id"])
            for row in rows
        }

        required_players = {
            "Sample India Batter",
            "Sample Australia Bowler",
        }

        if not required_players.issubset(player_ids):
            raise ValueError(
                "Please seed the sample teams, players, and match first."
            )

        stats = [
            (player_ids["Sample India Batter"][0],
             player_ids["Sample India Batter"][1],
             75, 50, 0, 0.0),
            (player_ids["Sample Australia Bowler"][0],
             player_ids["Sample Australia Bowler"][1],
             0, 0, 2, 4.0),
        ]

        connection.executemany(
            """
            INSERT INTO player_stats (
                player_id, match_id, runs, balls_faced,
                wickets, overs_bowled
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(player_id, match_id) DO NOTHING
            """,
            stats,
        )

        connection.commit()
        print("Sample player statistics added successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_player_stats()
