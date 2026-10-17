
from app.database.connection import get_connection
from app.database.seed_data import seed_teams


def test_seed_teams_inserts_sample_teams():
    seed_teams()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT team_name, country
            FROM teams
            WHERE team_name IN ('India', 'Australia')
            ORDER BY team_name
            """
        ).fetchall()

        teams = {
            row["team_name"]: row["country"]
            for row in rows
        }

        assert teams == {
            "Australia": "Australia",
            "India": "India",
        }

    finally:
        connection.close()
