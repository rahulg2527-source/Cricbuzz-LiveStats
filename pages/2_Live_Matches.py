import streamlit as st
import pandas as pd

from app.database.queries import get_all_matches


st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="\U0001F3CF",
    layout="wide",
)

st.title("\U0001F3CF Live Matches")
st.caption("Match information currently stored in the local database.")

try:
    matches = get_all_matches()

    if not matches:
        st.info(
            "No matches are available yet. "
            "Add match data to the database to see it here."
        )
    else:
        matches_df = pd.DataFrame(matches)

        total_matches = len(matches_df)
        live_matches = int(
            (matches_df["status"] == "live").sum()
        )
        scheduled_matches = int(
            (matches_df["status"] == "scheduled").sum()
        )
        completed_matches = int(
            (matches_df["status"] == "completed").sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Matches", total_matches)
        col2.metric("Live", live_matches)
        col3.metric("Scheduled", scheduled_matches)
        col4.metric("Completed", completed_matches)

        st.subheader("Match List")

        status_options = ["All"] + sorted(
            matches_df["status"].dropna().unique().tolist()
        )

        selected_status = st.selectbox(
            "Filter by match status",
            status_options,
        )

        filtered_df = matches_df.copy()

        if selected_status != "All":
            filtered_df = filtered_df[
                filtered_df["status"] == selected_status
            ]

        display_columns = [
            "match_id",
            "team1",
            "team2",
            "venue",
            "match_date",
            "status",
        ]

        st.dataframe(
            filtered_df[display_columns],
            width="stretch",
            hide_index=True,
        )

        csv_data = filtered_df[display_columns].to_csv(index=False)

        st.download_button(
            label="Download matches as CSV",
            data=csv_data,
            file_name="cricbuzz_matches.csv",
            mime="text/csv",
        )

        st.caption(
            "This page displays database records. "
            "Live score updates require Cricbuzz API integration."
        )

except Exception:
    st.error("Unable to load matches from the database.")
    st.exception(Exception("Please check the terminal for the underlying error."))