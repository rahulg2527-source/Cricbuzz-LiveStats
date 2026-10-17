
import sqlite3

import pandas as pd
import streamlit as st

from app.database.connection import get_connection


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="CRUD Operations | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

st.title("🏏 CRUD Operations")
st.write(
    "Manage teams and players in the Cricbuzz LiveStats database. "
    "All database changes are committed only after successful operations."
)


# ---------------------------------------------------------
# DATABASE HELPERS
# ---------------------------------------------------------
PLAYER_ROLES = [
    "Batter",
    "Bowler",
    "All-rounder",
    "Wicketkeeper",
]


def fetch_all(query, params=()):
    """Fetch database rows and return them as dictionaries."""
    connection = None
    try:
        connection = get_connection()
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if connection is not None:
            connection.close()


def execute_change(query, params=()):
    """Execute one database change inside a transaction."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.execute(query, params)
        affected_rows = cursor.rowcount
        connection.commit()
        return affected_rows
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if connection is not None:
            connection.close()


def show_database_error(error):
    """Display a helpful message for common database errors."""
    if isinstance(error, sqlite3.IntegrityError):
        st.error(
            "The operation could not be completed because of a database "
            "constraint. Check for duplicate names or related records."
        )
    elif isinstance(error, sqlite3.Error):
        st.error(f"Database error: {error}")
    else:
        st.error(f"Unexpected error: {error}")


def load_teams():
    return fetch_all(
        """
        SELECT team_id, team_name, country
        FROM teams
        ORDER BY team_name
        """
    )


def load_players():
    return fetch_all(
        """
        SELECT
            p.player_id,
            p.player_name,
            p.role,
            p.team_id,
            t.team_name
        FROM players AS p
        LEFT JOIN teams AS t
            ON p.team_id = t.team_id
        ORDER BY p.player_name, p.player_id
        """
    )


def team_name_exists(team_name, exclude_team_id=None):
    """Check for a team name without case or surrounding-space differences."""
    query = """
        SELECT team_id
        FROM teams
        WHERE LOWER(TRIM(team_name)) = LOWER(TRIM(?))
    """
    params = [team_name]

    if exclude_team_id is not None:
        query += " AND team_id != ?"
        params.append(exclude_team_id)

    query += " LIMIT 1"
    return bool(fetch_all(query, tuple(params)))


def player_name_exists(player_name, exclude_player_id=None):
    """Check for a duplicate player name, ignoring case and extra spaces."""
    query = """
        SELECT player_id
        FROM players
        WHERE LOWER(TRIM(player_name)) = LOWER(TRIM(?))
    """
    params = [player_name]

    if exclude_player_id is not None:
        query += " AND player_id != ?"
        params.append(exclude_player_id)

    query += " LIMIT 1"
    return bool(fetch_all(query, tuple(params)))


# ---------------------------------------------------------
# LOAD INITIAL DATA
# ---------------------------------------------------------
try:
    teams = load_teams()
    players = load_players()
except (sqlite3.Error, OSError) as error:
    st.error(f"Could not load database records: {error}")
    st.stop()


team_options = {
    team["team_id"]: team["team_name"]
    for team in teams
}


# ---------------------------------------------------------
# TEAM MANAGEMENT
# ---------------------------------------------------------
st.header("🏟️ Team Management")

team_create_tab, team_view_tab, team_update_tab, team_delete_tab = (
    st.tabs(
        [
            "➕ Create Team",
            "📋 View Teams",
            "✏️ Update Team",
            "🗑️ Delete Team",
        ]
    )
)


# CREATE TEAM
with team_create_tab:
    st.subheader("Add a New Team")

    with st.form("create_team_form"):
        new_team_name = st.text_input(
            "Team Name",
            placeholder="For example, India",
        )
        new_team_country = st.text_input(
            "Country",
            placeholder="For example, India",
        )

        create_team_submitted = st.form_submit_button(
            "Add Team",
            type="primary",
        )

    if create_team_submitted:
        team_name = new_team_name.strip()
        country = new_team_country.strip() or None

        if not team_name:
            st.warning("Please enter a team name.")
        else:
            try:
                if team_name_exists(team_name):
                    st.warning(
                        "A team with this name already exists."
                    )
                else:
                    execute_change(
                        """
                        INSERT INTO teams (team_name, country)
                        VALUES (?, ?)
                        """,
                        (team_name, country),
                    )
                    st.success(
                        f"Team '{team_name}' added successfully."
                    )
                    st.rerun()
            except (sqlite3.Error, OSError) as error:
                show_database_error(error)


# VIEW TEAMS
with team_view_tab:
    st.subheader("All Teams")

    try:
        current_teams = load_teams()

        if current_teams:
            st.dataframe(
                pd.DataFrame(current_teams),
                hide_index=True,
                width="stretch",
            )
            st.caption(f"Total teams: {len(current_teams)}")
        else:
            st.info("No teams found. Add a team to get started.")
    except (sqlite3.Error, OSError) as error:
        show_database_error(error)


# UPDATE TEAM
with team_update_tab:
    st.subheader("Update Team Details")

    try:
        current_teams = load_teams()

        if not current_teams:
            st.info("There are no teams to update.")
        else:
            team_ids = [team["team_id"] for team in current_teams]
            team_by_id = {
                team["team_id"]: team for team in current_teams
            }

            selected_team_id = st.selectbox(
                "Select a team",
                options=team_ids,
                format_func=lambda team_id: (
                    f"{team_by_id[team_id]['team_name']} "
                    f"(ID: {team_id})"
                ),
                key="update_team_id",
            )

            selected_team = team_by_id[selected_team_id]

            with st.form("update_team_form"):
                updated_team_name = st.text_input(
                    "Team Name",
                    value=selected_team["team_name"],
                )
                updated_team_country = st.text_input(
                    "Country",
                    value=selected_team["country"] or "",
                )

                update_team_submitted = st.form_submit_button(
                    "Save Team Changes",
                    type="primary",
                )

            if update_team_submitted:
                team_name = updated_team_name.strip()
                country = updated_team_country.strip() or None

                if not team_name:
                    st.warning("Team name cannot be empty.")
                else:
                    try:
                        if team_name_exists(
                            team_name,
                            exclude_team_id=selected_team_id,
                        ):
                            st.warning(
                                "Another team already uses this name."
                            )
                        else:
                            affected = execute_change(
                                """
                                UPDATE teams
                                SET team_name = ?, country = ?
                                WHERE team_id = ?
                                """,
                                (
                                    team_name,
                                    country,
                                    selected_team_id,
                                ),
                            )

                            if affected == 0:
                                st.warning(
                                    "Team not found. Refresh and retry."
                                )
                            else:
                                st.success(
                                    f"Team '{team_name}' updated successfully."
                                )
                                st.rerun()
                    except (sqlite3.Error, OSError) as error:
                        show_database_error(error)

    except (sqlite3.Error, OSError) as error:
        show_database_error(error)


# DELETE TEAM
with team_delete_tab:
    st.subheader("Delete a Team")
    st.warning(
        "Deleting a team sets its players' team_id to NULL. "
        "A team used by a match may not be deletable because of "
        "database foreign-key constraints."
    )

    try:
        current_teams = load_teams()

        if not current_teams:
            st.info("There are no teams to delete.")
        else:
            team_ids = [team["team_id"] for team in current_teams]
            team_by_id = {
                team["team_id"]: team for team in current_teams
            }

            delete_team_id = st.selectbox(
                "Select a team to delete",
                options=team_ids,
                format_func=lambda team_id: (
                    f"{team_by_id[team_id]['team_name']} "
                    f"(ID: {team_id})"
                ),
                key="delete_team_id",
            )

            delete_team_name = team_by_id[delete_team_id]["team_name"]

            with st.form("delete_team_form"):
                confirm_team_name = st.text_input(
                    f"Type {delete_team_name} to confirm",
                    key="confirm_delete_team_name",
                )
                delete_team_submitted = st.form_submit_button(
                    "Delete Selected Team",
                    type="primary",
                )

            if delete_team_submitted:
                if confirm_team_name.strip() != delete_team_name:
                    st.error(
                        "The confirmation name does not match. "
                        "The team was not deleted."
                    )
                else:
                    try:
                        affected = execute_change(
                            """
                            DELETE FROM teams
                            WHERE team_id = ? AND team_name = ?
                            """,
                            (delete_team_id, delete_team_name),
                        )

                        if affected == 0:
                            st.warning(
                                "Team not found. Refresh and retry."
                            )
                        else:
                            st.success(
                                f"Team '{delete_team_name}' deleted successfully."
                            )
                            st.rerun()
                    except (sqlite3.Error, OSError) as error:
                        show_database_error(error)

    except (sqlite3.Error, OSError) as error:
        show_database_error(error)


# ---------------------------------------------------------
# PLAYER MANAGEMENT
# ---------------------------------------------------------
st.divider()
st.header("🧑‍🏏 Player Management")

player_create_tab, player_view_tab, player_update_tab, player_delete_tab = (
    st.tabs(
        [
            "➕ Add Player",
            "📋 View Players",
            "✏️ Update Player",
            "🗑️ Delete Player",
        ]
    )
)


# ADD PLAYER
with player_create_tab:
    st.subheader("Add a New Player")

    if not teams:
        st.warning("Add a team before assigning a player to a team.")
    else:
        with st.form("create_player_form"):
            new_player_name = st.text_input(
                "Player Name",
                placeholder="For example, Sample Player",
            )
            new_player_role = st.selectbox(
                "Player Role",
                options=PLAYER_ROLES,
            )
            new_player_team_id = st.selectbox(
                "Team",
                options=list(team_options.keys()),
                format_func=lambda team_id: team_options[team_id],
            )

            create_player_submitted = st.form_submit_button(
                "Add Player",
                type="primary",
            )

        if create_player_submitted:
            player_name = new_player_name.strip()

            if not player_name:
                st.warning("Please enter a player name.")
            else:
                try:
                    if player_name_exists(player_name):
                        st.warning(
                            "A player with this name already exists."
                        )
                    else:
                        execute_change(
                            """
                            INSERT INTO players (
                                player_name,
                                role,
                                team_id
                            )
                            VALUES (?, ?, ?)
                            """,
                            (
                                player_name,
                                new_player_role,
                                new_player_team_id,
                            ),
                        )
                        st.success(
                            f"Player '{player_name}' added successfully."
                        )
                        st.rerun()
                except (sqlite3.Error, OSError) as error:
                    show_database_error(error)


# VIEW PLAYERS
with player_view_tab:
    st.subheader("All Players")

    try:
        current_players = load_players()

        if current_players:
            display_players = [
                {
                    "Player ID": player["player_id"],
                    "Player Name": player["player_name"],
                    "Role": player["role"],
                    "Team": player["team_name"] or "Unassigned",
                }
                for player in current_players
            ]

            st.dataframe(
                pd.DataFrame(display_players),
                hide_index=True,
                width="stretch",
            )
            st.caption(f"Total players: {len(current_players)}")
        else:
            st.info("No players found. Add a player to get started.")
    except (sqlite3.Error, OSError) as error:
        show_database_error(error)


# UPDATE PLAYER
with player_update_tab:
    st.subheader("Update Player Details")

    try:
        current_players = load_players()

        if not current_players:
            st.info("There are no players to update.")
        else:
            player_ids = [
                player["player_id"] for player in current_players
            ]
            player_by_id = {
                player["player_id"]: player for player in current_players
            }

            selected_player_id = st.selectbox(
                "Select a player to update",
                options=player_ids,
                format_func=lambda player_id: (
                    f"{player_by_id[player_id]['player_name']} "
                    f"(ID: {player_id})"
                ),
                key="update_player_id",
            )

            selected_player = player_by_id[selected_player_id]

            with st.form("update_player_form"):
                updated_player_name = st.text_input(
                    "Player Name",
                    value=selected_player["player_name"],
                )

                current_role = selected_player["role"]
                role_index = (
                    PLAYER_ROLES.index(current_role)
                    if current_role in PLAYER_ROLES
                    else 0
                )

                updated_player_role = st.selectbox(
                    "Player Role",
                    options=PLAYER_ROLES,
                    index=role_index,
                )

                team_ids_for_update = [None] + list(team_options.keys())

                current_team_id = selected_player["team_id"]
                team_index = (
                    team_ids_for_update.index(current_team_id)
                    if current_team_id in team_ids_for_update
                    else 0
                )

                updated_player_team_id = st.selectbox(
                    "Team",
                    options=team_ids_for_update,
                    index=team_index,
                    format_func=lambda team_id: (
                        "Unassigned"
                        if team_id is None
                        else team_options[team_id]
                    ),
                )

                update_player_submitted = st.form_submit_button(
                    "Save Player Changes",
                    type="primary",
                )

            if update_player_submitted:
                player_name = updated_player_name.strip()

                if not player_name:
                    st.warning("Player name cannot be empty.")
                else:
                    try:
                        if player_name_exists(
                            player_name,
                            exclude_player_id=selected_player_id,
                        ):
                            st.warning(
                                "Another player already uses this name."
                            )
                        else:
                            affected = execute_change(
                                """
                                UPDATE players
                                SET player_name = ?,
                                    role = ?,
                                    team_id = ?
                                WHERE player_id = ?
                                """,
                                (
                                    player_name,
                                    updated_player_role,
                                    updated_player_team_id,
                                    selected_player_id,
                                ),
                            )

                            if affected == 0:
                                st.warning(
                                    "Player not found. Refresh and retry."
                                )
                            else:
                                st.success(
                                    f"Player '{player_name}' updated successfully."
                                )
                                st.rerun()
                    except (sqlite3.Error, OSError) as error:
                        show_database_error(error)

    except (sqlite3.Error, OSError) as error:
        show_database_error(error)


# DELETE PLAYER
with player_delete_tab:
    st.subheader("Delete a Player")
    st.warning(
        "A player with linked player statistics cannot be deleted "
        "while those statistics reference the player. This page "
        "does not intentionally delete linked statistics."
    )

    try:
        current_players = load_players()

        if not current_players:
            st.info("There are no players to delete.")
        else:
            player_ids = [
                player["player_id"] for player in current_players
            ]
            player_by_id = {
                player["player_id"]: player for player in current_players
            }

            delete_player_id = st.selectbox(
                "Select a player to delete",
                options=player_ids,
                format_func=lambda player_id: (
                    f"{player_by_id[player_id]['player_name']} "
                    f"(ID: {player_id})"
                ),
                key="delete_player_id",
            )

            selected_player_name = player_by_id[delete_player_id][
                "player_name"
            ]

            st.write(
                f"Selected player: **{selected_player_name}** "
                f"(ID: {delete_player_id})"
            )

            # Keep the confirmation field and submit button together.
            with st.form("delete_player_form"):
                confirm_player_name = st.text_input(
                    f"Type {selected_player_name} to confirm deletion",
                    key="confirm_delete_player_name",
                )

                delete_player_submitted = st.form_submit_button(
                    "Delete Selected Player",
                    type="primary",
                )

            if delete_player_submitted:
                if confirm_player_name.strip() != selected_player_name:
                    st.error(
                        "The confirmation name does not match. "
                        "The player was not deleted."
                    )
                else:
                    connection = None

                    try:
                        connection = get_connection()

                        cursor = connection.execute(
                            """
                            DELETE FROM players
                            WHERE player_id = ? AND player_name = ?
                            """,
                            (
                                delete_player_id,
                                selected_player_name,
                            ),
                        )

                        if cursor.rowcount != 1:
                            connection.rollback()
                            st.warning(
                                "Player not found or changed before deletion. "
                                "Refresh and retry."
                            )
                        else:
                            connection.commit()
                            st.success(
                                f"Player '{selected_player_name}' "
                                "deleted successfully."
                            )
                            st.rerun()

                    except sqlite3.IntegrityError:
                        if connection is not None:
                            connection.rollback()

                        st.error(
                            "Deletion blocked: this player has linked "
                            "statistics or another database relationship. "
                            "No linked records were intentionally deleted."
                        )

                    except sqlite3.Error as error:
                        if connection is not None:
                            connection.rollback()
                        st.error(f"Database error: {error}")

                    finally:
                        if connection is not None:
                            connection.close()

    except (sqlite3.Error, OSError) as error:
        show_database_error(error)
