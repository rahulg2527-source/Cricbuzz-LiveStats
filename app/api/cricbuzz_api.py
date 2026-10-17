
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_HOST = "cricbuzz-cricket.p.rapidapi.com"
LIVE_MATCHES_URL = f"https://{API_HOST}/matches/v1/live"


def get_live_matches():
    """Fetch match data from the Cricbuzz API."""
    api_key = os.getenv("RAPIDAPI_KEY")

    if not api_key:
        raise ValueError(
            "RAPIDAPI_KEY is missing. Check your .env file."
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

                matches.append({
                    "match_id": info.get("matchId"),
                    "series": info.get("seriesName", ""),
                    "match": info.get("matchDesc", ""),
                    "format": info.get("matchFormat", ""),
                    "team1": team1.get("teamName", "Unknown"),
                    "team2": team2.get("teamName", "Unknown"),
                    "state": info.get("state", "Unknown"),
                    "status": info.get("status", ""),
                    "venue": venue.get("ground", ""),
                    "city": venue.get("city", ""),
                })

    return matches
