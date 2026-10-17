
import streamlit as st
import pandas as pd

from app.api.cricbuzz_api import get_live_matches


st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="\U0001F3CF",
    layout="wide",
)

st.title("\U0001F3CF Cricbuzz Live Matches")
st.caption("Live scores and match updates powered by Cricbuzz.")

if st.button("Refresh Matches"):
    st.cache_data.clear()


@st.cache_data(ttl=60)
def load_matches():
    return get_live_matches()


def display_team_score(team_name, innings_list):
    st.markdown(f"**{team_name}**")

    if not innings_list:
        st.write("Score not available yet")
        return

    for innings in innings_list:
        score = innings.get("score", "N/A")
        overs = innings.get("overs")

        if overs is not None:
            st.write(f"**{score}** ({overs} overs)")
        else:
            st.write(f"**{score}**")


try:
    matches = load_matches()

    if not matches:
        st.info("The API returned no matches.")
    else:
        matches_df = pd.DataFrame(matches)

        live_df = matches_df[
            matches_df["state"].str.strip().str.lower()
            == "in progress"
        ].copy()

        col1, col2 = st.columns(2)
        col1.metric("Matches returned", len(matches_df))
        col2.metric("Matches in progress", len(live_df))

        st.subheader("Match List")

        status_options = ["All"] + sorted(
            matches_df["state"].dropna().unique().tolist()
        )

        selected_status = st.selectbox(
            "Filter by match state",
            status_options,
        )

        filtered_df = matches_df.copy()

        if selected_status == "In Progress":
            filtered_df = live_df
        elif selected_status != "All":
            filtered_df = filtered_df[
                filtered_df["state"] == selected_status
            ]

        for _, match in filtered_df.iterrows():
            with st.container(border=True):
                st.caption(
                    f"{match['series']} | {match['format']} | "
                    f"{match['match']}"
                )

                team1_col, vs_col, team2_col = st.columns([5, 1, 5])

                with team1_col:
                    display_team_score(
                        match["team1"],
                        match["team1_score"],
                    )

                with vs_col:
                    st.markdown("### VS")

                with team2_col:
                    display_team_score(
                        match["team2"],
                        match["team2_score"],
                    )

                st.write(f"**Status:** {match['state']}")
                st.write(
                    match["status"] or "Match status not available."
                )

                venue = match["venue"] or "Venue not available"
                city = match["city"]

                if city:
                    venue += f", {city}"

                st.caption(f"Venue: {venue}")

        st.subheader("Download Match Data")

        export_columns = [
            "match_id",
            "series",
            "match",
            "format",
            "team1",
            "team1_score",
            "team2",
            "team2_score",
            "state",
            "status",
            "venue",
            "city",
        ]

        export_df = matches_df[export_columns].copy()

        for column in ["team1_score", "team2_score"]:
            export_df[column] = export_df[column].apply(
                lambda value: str(value)
            )

        st.download_button(
            label="Download all matches as CSV",
            data=export_df.to_csv(index=False),
            file_name="cricbuzz_matches.csv",
            mime="text/csv",
        )

except Exception as error:
    st.error("Unable to load matches from the Cricbuzz API.")
    st.caption(f"Error type: {type(error).__name__}")
    st.info(
        "Check your internet connection and RapidAPI configuration."
    )
