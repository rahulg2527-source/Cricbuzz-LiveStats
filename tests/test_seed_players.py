
from app.database.connection import get_connection
from app.database.seed_players import seed_players


def test_sample_players_are_linked_to_correct_teams():
    seed_players()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT p.player_name, p.role, t.team_name
            FROM players AS p
            JOIN teams AS t ON p.team_id = t.team_id
            WHERE p.player_name IN (
                'Sample India Batter',
                'Sample Australia Bowler'
            )
            ORDER BY p.player_name
            """
        ).fetchall()

        players = {
            row["player_name"]: (row["role"], row["team_name"])
            for row in rows
        }

        assert players == {
            "Sample Australia Bowler": ("Bowler", "Australia"),
            "Sample India Batter": ("Batter", "India"),
        }

    finally:
        connection.close()
