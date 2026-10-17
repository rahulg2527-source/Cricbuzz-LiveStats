
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_HOST = "cricbuzz-cricket.p.rapidapi.com"
LIVE_MATCHES_URL = f"https://{API_HOST}/matches/v1/live"


def format_team_score(team_score):
    """Format all available innings for one team."""
    if not isinstance(team_score, dict):
        return []

    innings_list = []

    for innings_name, innings in team_score.items():
        if not isinstance(innings, dict):
            continue

        runs = innings.get("runs")
        wickets = innings.get("wickets")
        overs = innings.get("overs")

        if runs is None:
            continue

        score_text = str(runs)

        if wickets is not None:
            score_text += f"/{wickets}"

        innings_list.append({
            "innings": innings_name,
            "score": score_text,
            "overs": overs,
        })

    return innings_list


def get_live_matches():
    """Fetch match information and scores from Cricbuzz."""
    api_key = os.getenv("RAPIDAPI_KEY")

    if not api_key:
        raise ValueError(
            "RAPIDAPI_KEY is missing. Check your .env file "
            "or Streamlit Cloud Secrets."
        )

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST,
    }

    response = requests.get(
        LIVE_MATCHES_URL,
        headers=headers,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Unexpected API response format.")

    matches = []

    for match_type in data.get("typeMatches", []):
        if not isinstance(match_type, dict):
            continue

        for series in match_type.get("seriesMatches", []):
            if not isinstance(series, dict):
                continue

            wrapper = series.get("seriesAdWrapper", {})
            if not isinstance(wrapper, dict):
                continue

            for match in wrapper.get("matches", []):
                if not isinstance(match, dict):
                    continue

                info = match.get("matchInfo", {})
                if not isinstance(info, dict):
                    continue

                team1 = info.get("team1") or {}
                team2 = info.get("team2") or {}
                venue = info.get("venueInfo") or {}
                match_score = match.get("matchScore") or {}

                team1_score = format_team_score(
                    match_score.get("team1Score")
                )
                team2_score = format_team_score(
                    match_score.get("team2Score")
                )

                matches.append({
                    "match_id": info.get("matchId"),
                    "series": info.get("seriesName", ""),
                    "match": info.get("matchDesc", ""),
                    "format": info.get("matchFormat", ""),
                    "team1": team1.get("teamName", "Unknown"),
                    "team2": team2.get("teamName", "Unknown"),
                    "team1_score": team1_score,
                    "team2_score": team2_score,
                    "state": info.get("state", "Unknown"),
                    "status": info.get("status", ""),
                    "venue": venue.get("ground", ""),
                    "city": venue.get("city", ""),
                })

    return matches
