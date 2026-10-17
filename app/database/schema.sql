
-- 1. Store cricket teams.
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT
);

-- 2. Store player profiles.
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    role TEXT CHECK (
        role IN ('Batter', 'Bowler', 'All-rounder', 'Wicketkeeper')
    ),
    team_id INTEGER,
    FOREIGN KEY (team_id)
        REFERENCES teams(team_id)
        ON DELETE SET NULL
);

-- 3. Store matches.
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    venue TEXT,
    match_date TEXT,
    status TEXT NOT NULL DEFAULT 'scheduled'
        CHECK (status IN ('scheduled', 'live', 'completed')),
    CHECK (team1_id <> team2_id),
    FOREIGN KEY (team1_id)
        REFERENCES teams(team_id),
    FOREIGN KEY (team2_id)
        REFERENCES teams(team_id)
);

-- 4. Store each player's statistics for a match.
CREATE TABLE IF NOT EXISTS player_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    runs INTEGER NOT NULL DEFAULT 0 CHECK (runs >= 0),
    balls_faced INTEGER NOT NULL DEFAULT 0 CHECK (balls_faced >= 0),
    wickets INTEGER NOT NULL DEFAULT 0 CHECK (wickets >= 0),
    overs_bowled REAL NOT NULL DEFAULT 0 CHECK (overs_bowled >= 0),
    UNIQUE (player_id, match_id),
    FOREIGN KEY (player_id)
        REFERENCES players(player_id),
    FOREIGN KEY (match_id)
        REFERENCES matches(match_id)
);

-- Improve common lookup and join operations.
CREATE INDEX IF NOT EXISTS idx_players_team
    ON players(team_id);

CREATE INDEX IF NOT EXISTS idx_matches_date
    ON matches(match_date);

CREATE INDEX IF NOT EXISTS idx_player_stats_match
    ON player_stats(match_id);

CREATE INDEX IF NOT EXISTS idx_player_stats_player
    ON player_stats(player_id);
