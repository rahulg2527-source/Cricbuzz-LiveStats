from app.database.connection import get_connection


def get_all_teams():
    """Retrieve all teams from the database."""
    connection = get_connection()

    try:
        teams = connection.execute(
            """
            SELECT
                team_id,
                team_name,
                country
            FROM teams
            ORDER BY team_name
            """
        ).fetchall()

        return [dict(team) for team in teams]

    finally:
        connection.close()


def get_all_players():
    """Retrieve all players with their team names."""
    connection = get_connection()

    try:
        players = connection.execute(
            """
            SELECT
                p.player_id,
                p.player_name,
                p.role,
                t.team_name
            FROM players AS p
            LEFT JOIN teams AS t
                ON p.team_id = t.team_id
            ORDER BY p.player_name
            """
        ).fetchall()

        return [dict(player) for player in players]

    finally:
        connection.close()


def get_all_matches():
    """Retrieve matches with both participating team names."""
    connection = get_connection()

    try:
        matches = connection.execute(
            """
            SELECT
                m.match_id,
                team1.team_name AS team1,
                team2.team_name AS team2,
                m.venue,
                m.match_date,
                m.status
            FROM matches AS m
            JOIN teams AS team1
                ON m.team1_id = team1.team_id
            JOIN teams AS team2
                ON m.team2_id = team2.team_id
            ORDER BY m.match_date DESC
            """
        ).fetchall()

        return [dict(match) for match in matches]

    finally:
        connection.close()


def get_all_player_stats():
    """Retrieve player statistics with player, team, and match details."""
    connection = get_connection()

    try:
        stats = connection.execute(
            """
            SELECT
                ps.stat_id,
                p.player_name,
                p.role,
                t.team_name,
                m.match_id,
                m.venue,
                m.match_date,
                ps.runs,
                ps.balls_faced,
                ps.wickets,
                ps.overs_bowled
            FROM player_stats AS ps
            JOIN players AS p
                ON ps.player_id = p.player_id
            LEFT JOIN teams AS t
                ON p.team_id = t.team_id
            JOIN matches AS m
                ON ps.match_id = m.match_id
            ORDER BY ps.runs DESC, ps.wickets DESC
            """
        ).fetchall()

        return [dict(stat) for stat in stats]

    finally:
        connection.close()


def get_dashboard_counts():
    """Return the total number of teams, players, and matches."""
    connection = get_connection()

    try:
        counts = connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM teams) AS total_teams,
                (SELECT COUNT(*) FROM players) AS total_players,
                (SELECT COUNT(*) FROM matches) AS total_matches
            """
        ).fetchone()

        return dict(counts)

    finally:
        connection.close()
