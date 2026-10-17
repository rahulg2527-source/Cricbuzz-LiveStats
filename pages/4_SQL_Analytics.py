import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

from app.database.connection import get_connection


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SQL Analytics | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

st.title("SQL Queries & Analytics")
st.write(
    "Explore cricket data using SQL queries, "
    "relational joins, aggregate functions, and visualizations."
)


# --------------------------------------------------
# DATABASE HELPERS
# --------------------------------------------------

def run_query(sql):
    """Execute a read-only SQL query and return a DataFrame."""
    connection = get_connection()

    try:
        return pd.read_sql_query(sql, connection)
    finally:
        connection.close()


def show_query_result(number, title, description, sql):
    """Display SQL, run it on demand, and show the result."""
    st.divider()
    st.subheader(f"Query {number}: {title}")
    st.write(description)
    st.code(sql.strip(), language="sql")

    if st.button("Run Query", key=f"run_query_{number}"):
        try:
            result = run_query(sql)

            if result.empty:
                st.warning("The query executed successfully, but returned no rows.")
            else:
                st.success(f"Query executed successfully — {len(result)} row(s).")
                st.dataframe(result, hide_index=True, width="stretch")

            return result

        except (sqlite3.Error, pd.errors.DatabaseError) as error:
            st.error(f"Database query failed: {error}")

    return None


# --------------------------------------------------
# DATABASE CONNECTION STATUS
# --------------------------------------------------

try:
    connection = get_connection()
    connection.execute("SELECT 1")
    connection.close()
    st.success("Database connection successful.")
except sqlite3.Error as error:
    st.error(f"Unable to connect to the database: {error}")
    st.stop()


# --------------------------------------------------
# QUERY 1: DISPLAY ALL TEAMS
# --------------------------------------------------

teams_sql = """
SELECT
    team_id,
    team_name,
    country
FROM teams
ORDER BY team_name;
"""

show_query_result(
    1,
    "All Teams",
    "Display every team registered in the database.",
    teams_sql,
)


# --------------------------------------------------
# QUERY 2: PLAYERS WITH THEIR TEAMS
# --------------------------------------------------

players_teams_sql = """
SELECT
    p.player_id,
    p.player_name,
    t.team_name
FROM players AS p
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
ORDER BY t.team_name, p.player_name;
"""

show_query_result(
    2,
    "Players and Their Teams",
    "Use LEFT JOIN to display players and their associated teams.",
    players_teams_sql,
)


# --------------------------------------------------
# QUERY 3: PLAYER PERFORMANCE SUMMARY
# --------------------------------------------------

performance_sql = """
SELECT
    p.player_name,
    t.team_name,
    COALESCE(SUM(ps.runs), 0) AS total_runs,
    COALESCE(SUM(ps.balls_faced), 0) AS total_balls_faced,
    COALESCE(SUM(ps.wickets), 0) AS total_wickets,
    COALESCE(SUM(ps.overs_bowled), 0) AS total_overs_bowled
FROM players AS p
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
LEFT JOIN player_stats AS ps
    ON p.player_id = ps.player_id
GROUP BY
    p.player_id,
    p.player_name,
    t.team_name
ORDER BY total_runs DESC, total_wickets DESC;
"""

show_query_result(
    3,
    "Player Performance Summary",
    "Calculate each player's recorded runs, balls faced, wickets, and overs.",
    performance_sql,
)


# --------------------------------------------------
# QUERY 4: MATCH SCHEDULE
# --------------------------------------------------

matches_sql = """
SELECT
    m.match_id,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    m.match_date,
    m.venue,
    m.status
FROM matches AS m
LEFT JOIN teams AS t1
    ON m.team1_id = t1.team_id
LEFT JOIN teams AS t2
    ON m.team2_id = t2.team_id
ORDER BY m.match_date DESC;
"""

show_query_result(
    4,
    "Match Schedule",
    "Display match dates, participating teams, venues, and statuses.",
    matches_sql,
)


# --------------------------------------------------
# QUERY 5: TOP 10 RUN SCORERS
# --------------------------------------------------

top_runs_sql = """
SELECT
    p.player_name,
    t.team_name,
    SUM(ps.runs) AS total_runs
FROM player_stats AS ps
JOIN players AS p
    ON ps.player_id = p.player_id
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
GROUP BY p.player_id, p.player_name, t.team_name
ORDER BY total_runs DESC
LIMIT 10;
"""

show_query_result(
    5,
    "Top 10 Run Scorers",
    "Rank players by the total runs recorded in player_stats.",
    top_runs_sql,
)


# --------------------------------------------------
# QUERY 6: TOP 10 WICKET TAKERS
# --------------------------------------------------

top_wickets_sql = """
SELECT
    p.player_name,
    t.team_name,
    SUM(ps.wickets) AS total_wickets
FROM player_stats AS ps
JOIN players AS p
    ON ps.player_id = p.player_id
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
GROUP BY p.player_id, p.player_name, t.team_name
ORDER BY total_wickets DESC
LIMIT 10;
"""

show_query_result(
    6,
    "Top 10 Wicket Takers",
    "Rank players by the total wickets recorded in player_stats.",
    top_wickets_sql,
)


# --------------------------------------------------
# QUERY 7: MATCH COUNTS BY STATUS
# --------------------------------------------------

match_status_sql = """
SELECT
    status,
    COUNT(*) AS total_matches
FROM matches
GROUP BY status
ORDER BY total_matches DESC, status;
"""

show_query_result(
    7,
    "Matches by Status",
    "Count matches classified as scheduled, live, or completed.",
    match_status_sql,
)


# --------------------------------------------------
# QUERY 8: NUMBER OF PLAYERS PER TEAM
# --------------------------------------------------

players_per_team_sql = """
SELECT
    t.team_name,
    COUNT(p.player_id) AS total_players
FROM teams AS t
LEFT JOIN players AS p
    ON t.team_id = p.team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_players DESC, t.team_name;
"""

show_query_result(
    8,
    "Players Per Team",
    "Count players in each team, including teams with no registered players.",
    players_per_team_sql,
)


# --------------------------------------------------
# QUERY 9: BATTING STRIKE RATE
# --------------------------------------------------

strike_rate_sql = """
SELECT
    p.player_name,
    t.team_name,
    SUM(ps.runs) AS total_runs,
    SUM(ps.balls_faced) AS total_balls_faced,
    CASE
        WHEN SUM(ps.balls_faced) > 0
        THEN ROUND(
            100.0 * SUM(ps.runs) / SUM(ps.balls_faced),
            2
        )
        ELSE NULL
    END AS strike_rate
FROM player_stats AS ps
JOIN players AS p
    ON ps.player_id = p.player_id
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
GROUP BY p.player_id, p.player_name, t.team_name
ORDER BY strike_rate DESC;
"""

show_query_result(
    9,
    "Batting Strike Rate",
    "Calculate runs scored per 100 balls faced. Players with zero recorded "
    "balls have a NULL strike rate.",
    strike_rate_sql,
)


# --------------------------------------------------
# QUERY 10: AVERAGE RUNS PER RECORDED STAT ROW
# --------------------------------------------------

average_runs_sql = """
SELECT
    p.player_name,
    t.team_name,
    ROUND(AVG(ps.runs), 2) AS average_runs_per_stat_row,
    COUNT(ps.runs) AS recorded_stat_rows
FROM players AS p
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
LEFT JOIN player_stats AS ps
    ON p.player_id = ps.player_id
GROUP BY p.player_id, p.player_name, t.team_name
ORDER BY average_runs_per_stat_row DESC;
"""

show_query_result(
    10,
    "Average Runs Per Recorded Stat Row",
    "Calculate the average runs per player_stats row. This is NOT the official "
    "cricket batting average because the database does not record dismissals "
    "or innings.",
    average_runs_sql,
)


# --------------------------------------------------
# QUERY 11: BOWLING PERFORMANCE SUMMARY
# --------------------------------------------------

bowling_summary_sql = """
SELECT
    p.player_name,
    t.team_name,
    SUM(ps.overs_bowled) AS total_overs_bowled,
    SUM(ps.wickets) AS total_wickets,
    CASE
        WHEN SUM(ps.overs_bowled) > 0
        THEN ROUND(
            SUM(ps.wickets) / SUM(ps.overs_bowled),
            2
        )
        ELSE NULL
    END AS wickets_per_over
FROM player_stats AS ps
JOIN players AS p
    ON ps.player_id = p.player_id
LEFT JOIN teams AS t
    ON p.team_id = t.team_id
GROUP BY p.player_id, p.player_name, t.team_name
ORDER BY wickets_per_over DESC, total_wickets DESC;
"""

show_query_result(
    11,
    "Bowling Performance Summary",
    "Summarize overs bowled and wickets taken. Wickets per over is a "
    "descriptive metric, NOT the standard bowling economy rate.",
    bowling_summary_sql,
)


# --------------------------------------------------
# VISUAL ANALYTICS
# --------------------------------------------------

st.divider()
st.header("Visual Analytics")
st.write(
    "The charts below summarize the current data stored in the database."
)

try:
    performance_df = run_query(performance_sql)

    if not performance_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            runs_df = performance_df[
                performance_df["total_runs"] > 0
            ].sort_values("total_runs", ascending=True)

            if not runs_df.empty:
                runs_chart = px.bar(
                    runs_df,
                    x="total_runs",
                    y="player_name",
                    color="team_name",
                    orientation="h",
                    title="Total Runs by Player",
                    labels={
                        "total_runs": "Total Runs",
                        "player_name": "Player",
                        "team_name": "Team",
                    },
                    text="total_runs",
                )
                runs_chart.update_layout(
                    yaxis_title="",
                    xaxis_title="Runs",
                )
                st.plotly_chart(runs_chart, width="stretch")
            else:
                st.info("No recorded runs are available to plot.")

        with col2:
            wickets_df = performance_df[
                performance_df["total_wickets"] > 0
            ].sort_values("total_wickets", ascending=True)

            if not wickets_df.empty:
                wickets_chart = px.bar(
                    wickets_df,
                    x="total_wickets",
                    y="player_name",
                    color="team_name",
                    orientation="h",
                    title="Total Wickets by Player",
                    labels={
                        "total_wickets": "Total Wickets",
                        "player_name": "Player",
                        "team_name": "Team",
                    },
                    text="total_wickets",
                )
                wickets_chart.update_layout(
                    yaxis_title="",
                    xaxis_title="Wickets",
                )
                st.plotly_chart(wickets_chart, width="stretch")
            else:
                st.info("No recorded wickets are available to plot.")

    status_df = run_query(match_status_sql)

    if not status_df.empty:
        status_chart = px.pie(
            status_df,
            names="status",
            values="total_matches",
            title="Match Status Distribution",
            hole=0.35,
        )
        st.plotly_chart(status_chart, width="stretch")

except (sqlite3.Error, pd.errors.DatabaseError) as error:
    st.error(f"Unable to generate visual analytics: {error}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Cricbuzz LiveStats | SQL Analytics | "
    "Powered by Python, SQLite, Pandas, Streamlit, and Plotly"
)
