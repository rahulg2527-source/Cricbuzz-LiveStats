
from app.database.connection import get_connection
from app.database.seed_stats import seed_player_stats


def test_sample_player_stats_are_correct():
    seed_player_stats()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                p.player_name,
                t.team_name,
                m.venue,
                ps.runs,
                ps.balls_faced,
                ps.wickets,
                ps.overs_bowled
            FROM player_stats AS ps
            JOIN players AS p ON ps.player_id = p.player_id
            JOIN teams AS t ON p.team_id = t.team_id
            JOIN matches AS m ON ps.match_id = m.match_id
            WHERE m.venue = 'Sample Cricket Ground'
            ORDER BY p.player_name
            """
        ).fetchall()

        stats = {
            row["player_name"]: (
                row["team_name"],
                row["runs"],
                row["balls_faced"],
                row["wickets"],
                row["overs_bowled"],
            )
            for row in rows
        }

        assert stats == {
            "Sample Australia Bowler": (
                "Australia", 0, 0, 2, 4.0
            ),
            "Sample India Batter": (
                "India", 75, 50, 0, 0.0
            ),
        }

    finally:
        connection.close()
