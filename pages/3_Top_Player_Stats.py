import streamlit as st
import pandas as pd
import plotly.express as px

from app.database.queries import get_all_player_stats


st.set_page_config(
    page_title="Top Player Stats | Cricbuzz LiveStats",
    page_icon="\U0001F3CF",
    layout="wide",
)

st.title("\U0001F3CF Top Player Stats")
st.caption(
    "Player performance from statistics stored in the local database."
)

try:
    stats = get_all_player_stats()

    if not stats:
        st.info(
            "No player statistics are available yet. "
            "Add player statistics to the database to see them here."
        )
    else:
        stats_df = pd.DataFrame(stats)

        # Dashboard metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Players with Statistics",
                stats_df["player_name"].nunique(),
            )

        with col2:
            st.metric(
                "Total Runs",
                int(stats_df["runs"].sum()),
            )

        with col3:
            st.metric(
                "Total Wickets",
                int(stats_df["wickets"].sum()),
            )

        # Filter players by team
        st.subheader("Player Performance")

        team_options = ["All"] + sorted(
            stats_df["team_name"].dropna().unique().tolist()
        )

        selected_team = st.selectbox(
            "Filter by team",
            team_options,
        )

        filtered_df = stats_df.copy()

        if selected_team != "All":
            filtered_df = filtered_df[
                filtered_df["team_name"] == selected_team
            ]

        # Sort player records
        sort_options = {
            "Most Runs": "runs",
            "Most Wickets": "wickets",
            "Most Balls Faced": "balls_faced",
        }

        selected_sort = st.selectbox(
            "Rank players by",
            list(sort_options.keys()),
        )

        filtered_df = filtered_df.sort_values(
            by=sort_options[selected_sort],
            ascending=False,
        )

        # Player statistics table
        display_columns = [
            "player_name",
            "team_name",
            "role",
            "runs",
            "balls_faced",
            "wickets",
            "overs_bowled",
            "venue",
            "match_date",
        ]

        st.dataframe(
            filtered_df[display_columns],
            width="stretch",
            hide_index=True,
        )

        # Aggregate runs for each player
        st.subheader("Runs by Player")

        runs_by_player = (
            filtered_df.groupby(
                "player_name",
                as_index=False,
            )["runs"]
            .sum()
            .sort_values("runs", ascending=True)
        )

        if not runs_by_player.empty:
            runs_chart = px.bar(
                runs_by_player,
                x="runs",
                y="player_name",
                orientation="h",
                text="runs",
                title="Total Runs Scored",
                labels={
                    "runs": "Runs",
                    "player_name": "Player Name",
                },
            )

            runs_chart.update_traces(
                textposition="outside",
                cliponaxis=False,
            )

            runs_chart.update_layout(
                yaxis={
                    "categoryorder": "total ascending",
                    "automargin": True,
                },
                xaxis_title="Runs",
                yaxis_title="Player Name",
                margin=dict(l=30, r=60, t=60, b=40),
                showlegend=False,
            )

            st.plotly_chart(
                runs_chart,
                width="stretch",
            )

        # Aggregate wickets for each player
        st.subheader("Wickets by Player")

        wickets_by_player = (
            filtered_df.groupby(
                "player_name",
                as_index=False,
            )["wickets"]
            .sum()
            .sort_values("wickets", ascending=True)
        )

        if not wickets_by_player.empty:
            wickets_chart = px.bar(
                wickets_by_player,
                x="wickets",
                y="player_name",
                orientation="h",
                text="wickets",
                title="Total Wickets Taken",
                labels={
                    "wickets": "Wickets",
                    "player_name": "Player Name",
                },
            )

            wickets_chart.update_traces(
                textposition="outside",
                cliponaxis=False,
            )

            wickets_chart.update_layout(
                yaxis={
                    "categoryorder": "total ascending",
                    "automargin": True,
                },
                xaxis_title="Wickets",
                yaxis_title="Player Name",
                margin=dict(l=30, r=60, t=60, b=40),
                showlegend=False,
            )

            st.plotly_chart(
                wickets_chart,
                width="stretch",
            )

        st.caption(
            "These figures come from local sample data. "
            "Live player statistics are not yet connected to Cricbuzz."
        )

except Exception:
    st.error("Unable to load player statistics from the database.")
    st.info(
        "Check the PowerShell terminal for the underlying error details."
    )
