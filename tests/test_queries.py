from app.database.queries import (
    get_all_teams,
    get_all_players,
    get_all_matches,
    get_all_player_stats,
    get_dashboard_counts,
)


def test_get_all_teams():
    """Check that all sample teams are returned."""
    teams = get_all_teams()

    team_names = [team["team_name"] for team in teams]

    assert "India" in team_names
    assert "Australia" in team_names
    assert len(teams) >= 2


def test_get_all_players():
    """Check that players are linked to the correct teams."""
    players = get_all_players()

    player_teams = {
        player["player_name"]: player["team_name"]
        for player in players
    }

    assert player_teams["Sample India Batter"] == "India"
    assert player_teams["Sample Australia Bowler"] == "Australia"


def test_get_all_matches():
    """Check that matches include the correct team names."""
    matches = get_all_matches()

    sample_matches = [
        match
        for match in matches
        if match["venue"] == "Sample Cricket Ground"
    ]

    assert len(sample_matches) >= 1

    match = sample_matches[0]

    assert match["team1"] == "India"
    assert match["team2"] == "Australia"
    assert match["status"] == "scheduled"


def test_get_all_player_stats():
    """Check that player statistics include correct player data."""
    stats = get_all_player_stats()

    india_batter = next(
        stat
        for stat in stats
        if stat["player_name"] == "Sample India Batter"
    )

    australia_bowler = next(
        stat
        for stat in stats
        if stat["player_name"] == "Sample Australia Bowler"
    )

    assert india_batter["team_name"] == "India"
    assert india_batter["runs"] == 75
    assert india_batter["balls_faced"] == 50

    assert australia_bowler["team_name"] == "Australia"
    assert australia_bowler["wickets"] == 2
    assert australia_bowler["overs_bowled"] == 4.0


def test_get_dashboard_counts():
    """Check dashboard counts against the current sample database."""
    counts = get_dashboard_counts()

    assert counts["total_teams"] == 7
    assert counts["total_players"] == 2
    assert counts["total_matches"] == 1
