from app.database.connection import get_connection


def seed_teams():
    """Insert sample international teams without creating duplicates."""
    teams = [
        ("India", "India"),
        ("Australia", "Australia"),
        ("England", "England"),
        ("South Africa", "South Africa"),
        ("New Zealand", "New Zealand"),
        ("Pakistan", "Pakistan"),
        ("Sri Lanka", "Sri Lanka"),
    ]

    connection = get_connection()

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.executemany(
            """
            INSERT INTO teams (team_name, country)
            VALUES (?, ?)
            ON CONFLICT(team_name) DO NOTHING
            """,
            teams,
        )

        connection.commit()
        print("Sample teams added successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_teams()
