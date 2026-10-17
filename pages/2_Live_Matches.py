
import streamlit as st
import pandas as pd

from app.api.cricbuzz_api import get_live_matches


st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="\U0001F3CF",
    layout="wide",
)

st.title("\U0001F3CF Cricbuzz Live Matches")
st.caption("Live match information from the Cricbuzz API.")

if st.button("Refresh Matches"):
    st.cache_data.clear()


@st.cache_data(ttl=60)
def load_matches():
    return get_live_matches()


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

        display_columns = [
            "match_id",
            "team1",
            "team2",
            "format",
            "venue",
            "state",
            "status",
        ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True,
        )

        csv_data = filtered_df[display_columns].to_csv(index=False)

        st.download_button(
            label="Download matches as CSV",
            data=csv_data,
            file_name="cricbuzz_live_matches.csv",
            mime="text/csv",
        )

except Exception as error:
    st.error("Unable to load matches from the Cricbuzz API.")
    st.caption(f"Error type: {type(error).__name__}")
    st.info(
        "Check your internet connection and RapidAPI configuration."
    )
