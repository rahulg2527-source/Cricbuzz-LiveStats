
from app.database.connection import get_connection
from app.database.seed_matches import seed_matches


def test_sample_match_has_correct_teams():
    seed_matches()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                t1.team_name AS team1,
                t2.team_name AS team2,
                m.venue,
                m.status
            FROM matches AS m
            JOIN teams AS t1 ON m.team1_id = t1.team_id
            JOIN teams AS t2 ON m.team2_id = t2.team_id
            WHERE t1.team_name = 'India'
              AND t2.team_name = 'Australia'
              AND m.match_date = '2026-10-15'
            """
        ).fetchone()

        assert row is not None
        assert row["team1"] == "India"
        assert row["team2"] == "Australia"
        assert row["venue"] == "Sample Cricket Ground"
        assert row["status"] == "scheduled"

    finally:
        connection.close()
