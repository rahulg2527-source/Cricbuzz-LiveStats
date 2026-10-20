# Cricbuzz LiveStats

## Complete Project Documentation—Step by Step

**Project Type:** Cricket Analytics and Live Score Dashboard
**Language:** Python
**Frontend:** Streamlit
**Database:** SQLite
**API:** Cricbuzz Cricket API via RapidAPI
**Data Processing:** Pandas
**Visualization:** Plotly (for analytics pages)
**Testing:** Pytest
**Deployment:** Streamlit Community Cloud
**Source Control:** Git and GitHub

**GitHub Repository:** [https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git](https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git)

**Live Application:** [https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/](https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/)

---

# 1. Project Overview

Cricbuzz LiveStats is a cricket analytics web application built using Python and Streamlit. It combines cricket match information from the Cricbuzz API with a relational SQLite database to provide a dashboard for match information, player statistics, SQL analytics, and database management.

The application has two main data sources:

1. **Cricbuzz API:** Supplies match information, team names, scores, overs, match status, and venue information when available.
2. **SQLite database:** Stores structured records for teams, players, matches, and player statistics.

The project is designed to demonstrate API integration, database design, Python programming, data analysis, automated testing, and web application deployment.

## 1.1 Project objectives

- Display cricket match information in a web interface.
- Retrieve match data from a third-party API.
- Display scores, innings, overs, and match status when available.
- Filter matches by state.
- Export match information as a CSV file.
- Store structured cricket data in SQLite.
- Perform SQL-based analytics.
- Support CRUD operations for database records.
- Deploy the application online.

## 1.2 Main technologies

| Technology                | Purpose                               |
| ------------------------- | ------------------------------------- |
| Python                    | Application logic and API integration |
| Streamlit                 | Interactive web interface             |
| SQLite                    | Relational database                   |
| SQL                       | Data queries and analytics            |
| Requests                  | HTTP requests to the Cricbuzz API     |
| Pandas                    | Data processing and tables            |
| Plotly                    | Interactive charts and visualizations |
| python-dotenv             | Load local environment variables      |
| Pytest                    | Automated testing                     |
| Git and GitHub            | Version control and source hosting    |
| Streamlit Community Cloud | Web application hosting               |

---

# 2. Project Architecture

The application follows a simple layered architecture.

```text
Cricbuzz LiveStats
        |
        v
Streamlit User Interface
        |
        +----------------------+
        |                      |
        v                      v
Cricbuzz API Module      Database Query Layer
        |                      |
        v                      v
RapidAPI Cricbuzz             SQLite
        |                      |
        v                      v
Match Data and Scores    Teams, Players,
                         Matches, Player Stats
```

## Explanation

**User interface:** Displays dashboards, match cards, tables, filters, and download controls.

**API module:** Sends requests to RapidAPI, processes JSON responses, and extracts match information.

**Database query layer:** Executes SQL queries to retrieve and manage structured cricket data.

**SQLite database:** Stores the project's local sample and application records.

**Testing layer:** Checks database behavior, schema integrity, and other implemented functionality.

---

# 3. Development Environment Setup

The project was developed on Windows using Python 3.12.10 and PowerShell.

## Step 1: Open the project directory

Open PowerShell and run:

```powershell
cd C:\Users\rahul\Projects\Cricbuzz-LiveStats
```

This changes the terminal's working directory to the project root.

## Step 2: Create a virtual environment

If you are setting up the project for the first time:

```powershell
python -m venv .venv
```

A virtual environment isolates the project's Python packages from other Python projects.

If `.venv` already exists, do not recreate it unnecessarily.

## Step 3: Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, PowerShell should display `(.venv)` before the command prompt.

## Step 4: Install dependencies

The project uses a `requirements.txt` file.

Install its dependencies with:

```powershell
python -m pip install -r requirements.txt
```

The dependency list includes:

- `streamlit`
- `pandas`
- `plotly`
- `requests`
- `python-dotenv`

## Step 5: Verify the environment

Run:

```powershell
python --version
```

Then:

```powershell
python -m pytest -q
```

The previously verified project test suite completed with 13 passing tests. If you make further changes, rerun the tests to confirm the current code still passes.

---

# 4. Project Folder Structure

The principal files and folders are organized as follows.

```text
Cricbuzz-LiveStats/
|
|-- main.py
|-- requirements.txt
|-- .gitignore
|-- .env
|
|-- app/
|   |-- __init__.py
|   |
|   |-- api/
|   |   |-- cricbuzz_api.py
|   |
|   |-- database/
|   |   |-- __init__.py
|   |   |-- connection.py
|   |   |-- queries.py
|   |   |-- init_db.py
|   |   |-- seed_data.py
|   |   |-- seed_players.py
|   |   |-- seed_matches.py
|   |   |-- seed_stats.py
|   |
|   |-- pages/
|       |-- 2_Live_Matches.py
|
|-- pages/
|   |-- 2_Live_Matches.py
|   |-- 3_Top_Player_Stats.py
|   |-- 4_SQL_Analytics.py
|   |-- 5_CRUD_Operations.py
|
|-- data/
|   |-- cricbuzz.db
|
|-- tests/
|
|-- test_live_api.py
|-- test_live_filter.py
|-- test_live_scores.py
```

*Note:* This is a conceptual overview of the files discussed during development. Some files may differ or be absent depending on your current working tree. The root-level `pages/2_Live_Matches.py` is the page we updated for the score-card interface.

## Important files

**`main.py`** — The home page and dashboard overview.

**`app/api/cricbuzz_api.py`** — Fetches and processes match data from the API.

**`app/database/connection.py`** — Creates SQLite connections.

**`app/database/queries.py`** — Provides reusable database queries.

**`pages/2_Live_Matches.py`** — Displays match cards, score information, filters, and CSV export.

**`pages/3_Top_Player_Stats.py`** — Player statistics page.

**`pages/4_SQL_Analytics.py`** — SQL query and analytics page.

**`pages/5_CRUD_Operations.py`** — Database management interface.

**`tests/`** — Contains automated tests for implemented functionality.

---

# 5. Database Design

SQLite is used as the project's relational database. It stores structured data in tables and supports relationships through primary and foreign keys.

The database contains four principal tables.

## 5.1 Teams table

Stores team information.

| Column      | Purpose                          |
| ----------- | -------------------------------- |
| `team_id`   | Primary key                      |
| `team_name` | Unique team name                 |
| `country`   | Country associated with the team |

The `team_id` uniquely identifies each team.

## 5.2 Players table

Stores player information.

| Column        | Purpose                         |
| ------------- | ------------------------------- |
| `player_id`   | Primary key                     |
| `player_name` | Player's name                   |
| `role`        | Playing role                    |
| `team_id`     | Foreign key referencing `teams` |

The allowed roles are Batter, Bowler, All-rounder, and Wicketkeeper.

The relationship between teams and players allows multiple players to be associated with a team. The `team_id` can be null where appropriate.

## 5.3 Matches table

Stores match information.

| Column       | Purpose                 |
| ------------ | ----------------------- |
| `match_id`   | Primary key             |
| `team1_id`   | First team foreign key  |
| `team2_id`   | Second team foreign key |
| `venue`      | Match venue             |
| `match_date` | Match date              |
| `status`     | Match status            |

The database schema supports the states `scheduled`, `live`, and `completed`.

A database constraint prevents a team from being scheduled against itself.

## 5.4 Player statistics table

Stores player performance for a match.

| Column         | Purpose                           |
| -------------- | --------------------------------- |
| `stat_id`      | Primary key                       |
| `player_id`    | Foreign key referencing `players` |
| `match_id`     | Foreign key referencing `matches` |
| `runs`         | Runs scored                       |
| `balls_faced`  | Balls faced                       |
| `wickets`      | Wickets taken                     |
| `overs_bowled` | Overs bowled                      |

The table has a uniqueness constraint on `(player_id, match_id)` so a player cannot have duplicate statistics records for the same match.

## 5.5 Relationships

```text
Teams
  |
  | team_id
  v
Players
  |
  | player_id
  v
Player Stats
  ^
  | match_id
  |
Matches
```

Conceptually:

- A team can have multiple players.
- A player can have statistics for multiple matches.
- A match can contain statistics for multiple players.

The database enables relational queries, filtering, aggregation, and reporting.

---

# 6. Database Initialization and Sample Data

## Step 1: Understand the connection utility

The connection utility is located at:

```text
app/database/connection.py
```

It provides a reusable `get_connection()` function.

The function:

1. Resolves the project root directory.
2. Identifies the SQLite database file.
3. Creates the data directory if needed.
4. Opens a database connection.
5. Enables SQLite foreign-key enforcement.
6. Configures rows to be accessible by column name.

Enabling foreign keys helps protect relationships between database tables.

## Step 2: Initialize the schema

Run:

```powershell
python -m app.database.init_db
```

This initializes the database schema through the project's initialization module.

## Step 3: Add sample records

The project has separate modules for seeding sample records:

```powershell
python -m app.database.seed_data
```

```powershell
python -m app.database.seed_players
```

```powershell
python -m app.database.seed_matches
```

```powershell
python -m app.database.seed_stats
```

Run each command from the project root with the virtual environment active.

These commands should be used according to their implementation and current database state. Review their behavior before rerunning them if they are not designed to be idempotent.

---

# 7. Cricbuzz API Integration

The project integrates the Cricbuzz Cricket API through RapidAPI.

**API host:**

```text
cricbuzz-cricket.p.rapidapi.com
```

**Verified live-matches endpoint:**

```text
https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live
```

**HTTP method:** GET

## 7.1 API authentication

RapidAPI requests use two headers:

```python
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": API_HOST,
}
```

The API key is loaded from an environment variable. It must never be hard-coded into a Python file or committed to GitHub.

## 7.2 Local environment configuration

Create or edit the `.env` file in the project root:

```text
RAPIDAPI_KEY=YOUR_ACTUAL_RAPIDAPI_KEY
```

Replace the placeholder with your real key.

The `.env` file should be excluded from version control through `.gitignore`.

## 7.3 API request process

The `get_live_matches()` function performs the following steps:

1. Loads the API key.
2. Checks that the key exists.
3. Builds the RapidAPI headers.
4. Sends a GET request.
5. Checks the HTTP response.
6. Parses the JSON response.
7. Traverses the nested match structure.
8. Extracts team names, match details, scores, and venue information.
9. Returns a list of dictionaries for use by the Streamlit interface.

## 7.4 Match fields

The API module extracts fields such as:

- `match_id`
- `series`
- `match`
- `format`
- `team1`
- `team2`
- `team1_score`
- `team2_score`
- `state`
- `status`
- `venue`
- `city`

The scores are extracted from the API's `matchScore` object.

## 7.5 Score formatting

A team's innings data is converted into a list of dictionaries containing the innings identifier, score, and overs.

For example:

```python
{
    "innings": "inngs1",
    "score": "256/10",
    "overs": 49.6
}
```

The score display uses the values supplied by the API. Cricket overs should not be treated as decimal fractions when doing calculations; for display, the source value is retained.

**Important limitation:** The live-matches endpoint may return matches in different states, including completed matches and fixtures. The application filters matches by the state returned by the provider rather than assuming that every returned match is currently live.

---

# 8. Live Matches User Interface

The Live Matches page is the primary API-powered interface.

It displays the match information retrieved through `get_live_matches()`.

## 8.1 Match cards

Each match card can display:

- Series name
- Match description
- Format
- First team's name and score
- Second team's name and score
- Innings and overs where available
- Match state
- Current status message
- Venue and city

If the API does not provide a team's score, the interface can display a fallback message rather than inventing a score.

## 8.2 Match-state filter

The page provides a dropdown filter based on the match states returned by the API.

Users can select `All` or a specific state.

For the `In Progress` state, the page displays only records marked as in progress by the provider.

## 8.3 Refresh functionality

The refresh button clears Streamlit's data cache so the next data load requests updated information.

The data-loading function uses a 60-second cache to reduce unnecessary API calls during normal reruns.

The API subscription has a request quota, so caching helps limit usage.

## 8.4 CSV export

The application allows the displayed match data to be downloaded as a CSV file.

The export includes match identifiers, series and format details, team names, score information, state, status, and venue fields.

The CSV is generated using Pandas.

---

# 9. Streamlit Dashboard

The application is launched from `main.py`.

The home page displays the project title and a dashboard overview.

The dashboard queries the SQLite database for counts such as:

- Total teams
- Total players
- Total matches

The home page's database counts are distinct from the live API feed. They should not be interpreted as counts of current live fixtures.

## Launch the application

From the project root, run:

```powershell
python -m streamlit run main.py
```

Streamlit prints a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

---

# 10. Top Player Statistics

The Top Player Stats page is part of the project's analytics interface.

Its purpose is to present player performance information using the structured player statistics data.

The database supports fields such as runs, balls faced, wickets, and overs bowled. These fields can be queried to calculate or compare player performance.

The exact statistics, ranking formulas, and filters depend on the implementation of the current page.

---

# 11. SQL Analytics

The SQL Analytics page demonstrates how relational queries can answer cricket-related questions.

Typical analytics supported by the database schema include:

- Counting teams, players, and matches.
- Retrieving matches by status.
- Comparing team and player records.
- Aggregating player runs.
- Ranking players by performance.
- Identifying players with high wicket counts.
- Joining players, teams, matches, and statistics.

For example, a basic query to retrieve player run totals is:

```sql
SELECT
    p.player_name,
    SUM(ps.runs) AS total_runs
FROM players AS p
JOIN player_stats AS ps
    ON p.player_id = ps.player_id
GROUP BY p.player_id, p.player_name
ORDER BY total_runs DESC;
```

This query sums the stored runs for each player and sorts the results from highest to lowest.

The query is illustrative; its output depends on the records currently present in the database.

---

# 12. CRUD Operations

CRUD stands for:

- **Create:** Add a new record.
- **Read:** Retrieve an existing record.
- **Update:** Modify a record.
- **Delete:** Remove a record.

The CRUD Operations page provides an interface for managing database records.

The project has implemented team and player CRUD functionality during development.

For example:

1. A user enters the details for a new team.
2. The application validates the input.
3. A database operation inserts the record.
4. The interface refreshes the displayed records.
5. An update or delete action operates on the selected record.

Database constraints help prevent invalid data, including duplicate unique team names and invalid relationships.

---

# 13. Automated Testing

The project uses Pytest.

The previously verified test suite reported:

```text
13 passed in 2.68s
```

This result was obtained during development on October 17, 2026.

It confirms that the tests passed at that point, not that every future change is automatically verified.

## Step 1: Run the full test suite

```powershell
python -m pytest -q
```

## Step 2: Run a specific test

For example:

```powershell
python -m pytest tests/test_schema.py -v
```

Use the actual test file names present in your current project.

## Step 3: Test the API module

The following command checks that the module returns match records:

```powershell
python -c "from app.api.cricbuzz_api import get_live_matches; matches = get_live_matches(); print('Matches:', len(matches)); print('First match:', matches[0] if matches else 'No matches')"
```

This command requires a valid API key, network connectivity, and an active subscription.

## Step 4: Test score extraction

The project also includes a score test script:

```powershell
python test_live_scores.py
```

It inspects score information returned by the API.

## Step 5: Test the user interface manually

Run the Streamlit application and verify:

- The home page loads.
- The Live Matches page opens.
- Match cards display available scores.
- The state filter works.
- Refreshing requests updated information.
- CSV download works.
- The other project pages still function.

---

# 14. Git and GitHub

Git tracks changes to the source code. GitHub hosts the repository remotely.

The repository is:

[https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git](https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git)

## Step 1: Check repository status

```powershell
git status
```

## Step 2: Stage selected files

For example:

```powershell
git add app/api/cricbuzz_api.py pages/2_Live_Matches.py
```

Only stage files you intend to include in the commit.

## Step 3: Commit changes

```powershell
git commit -m "Describe the change"
```

A commit records the staged changes in local Git history.

## Step 4: Push to GitHub

```powershell
git push origin main
```

The push publishes the committed changes to the remote repository.

## Important security rule

Never commit:

- `.env`
- API keys
- Passwords
- Access tokens
- Other private credentials

The `.gitignore` file should exclude `.env`, the virtual environment, Python caches, and test caches.

---

# 15. Streamlit Community Cloud Deployment

The project is deployed at:

[https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/](https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/)

The deployment process uses GitHub as the source repository.

## Step 1: Maintain `requirements.txt`

The file must include the packages needed by the application, including `python-dotenv`, because the API module imports it.

## Step 2: Push the latest changes

After testing and committing the changes:

```powershell
git push origin main
```

Streamlit Cloud can then rebuild the application from the updated repository.

## Step 3: Configure cloud secrets

The local `.env` file is not automatically available on Streamlit Cloud.

In the app's management interface, open the Secrets editor and configure:

```toml
RAPIDAPI_KEY = "YOUR_ACTUAL_RAPIDAPI_KEY"
```

Replace the placeholder with the real key inside the cloud secrets editor.

Do not publish the real key in source code or this documentation.

## Step 4: Verify the deployment

Open the deployed app and test the Live Matches page.

Confirm that:

- The app finishes rebuilding.
- The API key is read correctly.
- Match data loads.
- Score cards render.
- Filtering works.
- CSV export works.

If deployment fails, check the Streamlit Cloud logs for the actual exception.

---

# 16. Troubleshooting Guide

## Problem 1: `ModuleNotFoundError`

**Cause:** A required package is missing from the current environment.

**Solution:**

```powershell
python -m pip install -r requirements.txt
```

Make sure the missing package is included in `requirements.txt` so that cloud deployments install it as well.

## Problem 2: API key is missing

**Cause:** `RAPIDAPI_KEY` is not available to the application.

**Solution:**

- Check the local `.env` file for local development.
- Check Streamlit Cloud Secrets for the deployed application.
- Confirm the variable name is exactly `RAPIDAPI_KEY`.
- Never print the key while debugging.

## Problem 3: HTTP 403

**Possible causes:**

- Invalid API key.
- Missing or inactive API subscription.
- API access restrictions.

Check the RapidAPI subscription and authentication configuration.

## Problem 4: HTTP 404

**Possible cause:** Incorrect API host, version, or endpoint path.

The verified endpoint used in this project is:

```text
/matches/v1/live
```

## Problem 5: No score available

**Cause:** The API response may not contain score data for that match.

**Solution:** Show a clear fallback message and preserve the match information that is available.

## Problem 6: Streamlit page shows old content

**Possible causes:**

- A different page file is being used.
- The browser is displaying stale content.
- The latest changes have not been deployed.

Check the active page path, refresh the browser, and confirm that the GitHub push and cloud rebuild completed.

## Problem 7: Tests fail

Run:

```powershell
python -m pytest -v
```

Read the first failing test and its traceback. Identify the underlying problem before modifying unrelated files.

---

# 17. Current Limitations and Considerations

1. **API quota:** The RapidAPI subscription has a request limit. Avoid unnecessary repeated API calls.
2. **Changing data:** Match states, scores, and the number of returned matches change over time.
3. **Score availability:** Scores may be absent for some matches.
4. **Database persistence:** The local SQLite database is suitable for development, but a deployed Streamlit Cloud instance may not provide durable persistence for database writes across rebuilds or instance changes.
5. **Separate data sources:** API match data and local database match records are not automatically synchronized merely because both are displayed by the application.
6. **Credentials:** The API key must remain in local environment configuration or cloud secrets, never in GitHub source files.
7. **Testing:** Automated tests should be rerun after modifications. A successful test run does not replace manual testing of the deployed interface.

---

# 18. Project Development Timeline

The project was developed incrementally.

**Phase 1 — Environment and setup**

- Created the project environment.
- Installed Python dependencies.
- Established the initial folder structure.

**Phase 2 — Database**

- Created the SQLite connection utility.
- Designed the four-table schema.
- Added database initialization and sample data.
- Implemented query functions and tests.

**Phase 3 — Application pages**

- Built the home dashboard.
- Implemented the match listing and database-related pages.
- Added SQL analytics and CRUD functionality.

**Phase 4 — API integration**

- Configured RapidAPI.
- Verified the live-matches endpoint.
- Created `app/api/cricbuzz_api.py`.
- Extracted match data and scores.

**Phase 5 — UI enhancements**

- Integrated API data into the Live Matches page.
- Added score cards, match-state filtering, refresh, and CSV export.
- Ran the automated test suite.

**Phase 6 — Version control and deployment**

- Committed the changes to Git.
- Pushed the code to GitHub.
- Configured dependencies and cloud secrets.
- Verified that the deployed application could retrieve match data.

---

# 19. Future Improvements

Potential future enhancements include:

- Better score-card styling and team logos.
- More detailed innings and score breakdowns.
- Player statistics sourced from a suitable API endpoint.
- Automatic synchronization between API data and the database.
- More advanced SQL visualizations.
- Improved validation and error messages.
- More automated tests for API parsing and UI data handling.
- A persistent production database if cloud write operations become important.
- API response caching and quota monitoring.
- Deployment monitoring and logging.

These are potential improvements, not claims that every feature has already been implemented.

---

# 20. Conclusion

Cricbuzz LiveStats is a Python-based cricket dashboard combining API integration, relational database design, analytics, and an interactive web interface.

The project demonstrates practical skills in Python, SQL, SQLite, REST API requests, Pandas, Streamlit, testing, Git, GitHub, and cloud deployment.

The most important engineering lesson is to build the application incrementally: establish the database, verify individual components, integrate the API, test each change, and deploy only after confirming that the relevant functionality works.

**Project links**

- GitHub: [https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git](https://github.com/rahulg2527-source/Cricbuzz-LiveStats.git)
- Deployed application: [https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/](https://cricbuzz-livestats-qkwbzrxxv8s9unb2eeknkm.streamlit.app/)
