
import streamlit as st
import pandas as pd

from app.api.cricbuzz_api import get_live_matches

st.set_page_config(
    page_title="Live Cricket Matches",
    page_icon="🏏",
    layout="wide",
)

st.title("🏏 Cricbuzz Live Matches")
st.write("Live match information powered by the Cricbuzz API.")

if st.button("🔄 Refresh Matches"):
    st.cache_data.clear()

@st.cache_data(ttl=60)
def load_matches():
    return get_live_matches()

try:
    matches = load_matches()

    if not matches:
        st.info("No matches were returned by the API.")
    else:
        df = pd.DataFrame(matches)

        live_df = df[
            df["state"].str.strip().str.lower() == "in progress"
        ].copy()

        st.metric("Matches returned by API", len(df))
        st.metric("Matches in progress", len(live_df))

        if live_df.empty:
            st.info("There are currently no matches marked In Progress.")
        else:
            for _, match in live_df.iterrows():
                with st.container(border=True):
                    st.subheader(
                        f"{match['team1']} vs {match['team2']}"
                    )

                    st.write(
                        f"**Format:** {match['format'] or 'Not available'}"
                    )
                    st.write(
                        f"**Match:** {match['match'] or 'Not available'}"
                    )
                    st.write(
                        f"**Venue:** {match['venue'] or 'Not available'}"
                    )
                    st.write(
                        f"**Status:** {match['status'] or 'Not available'}"
                    )

        with st.expander("View all matches returned by the API"):
            st.dataframe(df, use_container_width=True)

except Exception as error:
    st.error("Unable to load matches from the Cricbuzz API.")
    st.caption(f"Error type: {type(error).__name__}")
    st.info(
        "Check your internet connection, API subscription, "
        "and local .env configuration."
    )
