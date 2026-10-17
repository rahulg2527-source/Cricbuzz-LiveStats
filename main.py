import streamlit as st

from app.database.queries import get_dashboard_counts


st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="\U0001F3CF",
    layout="wide",
)

st.title("\U0001F3CF Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.info(
    "Welcome! We are building a cricket analytics dashboard "
    "with live matches, player statistics, and SQL analytics."
)

st.write("## Dashboard Overview")

try:
    counts = get_dashboard_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Teams",
            value=counts["total_teams"],
        )

    with col2:
        st.metric(
            label="Total Players",
            value=counts["total_players"],
        )

    with col3:
        st.metric(
            label="Total Matches",
            value=counts["total_matches"],
        )

except Exception as error:
    st.error(
        "Unable to load dashboard statistics. "
        "Please check the database connection."
    )
    st.exception(error)

st.write("## Project Status")
st.write("Database connection and query layer implemented.")
st.caption(
    "The current figures come from local sample data. "
    "Live Cricbuzz API integration is not yet implemented."
)
