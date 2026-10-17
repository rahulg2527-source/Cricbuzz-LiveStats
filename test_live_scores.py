
import requests

from app.api.cricbuzz_api import API_HOST, LIVE_MATCHES_URL
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": API_HOST,
}

response = requests.get(
    LIVE_MATCHES_URL,
    headers=headers,
    timeout=20,
)

print("HTTP status:", response.status_code)
response.raise_for_status()

data = response.json()

for match_type in data.get("typeMatches", []):
    for series in match_type.get("seriesMatches", []):
        wrapper = series.get("seriesAdWrapper", {})
        for match in wrapper.get("matches", []):
            info = match.get("matchInfo", {})
            score = match.get("matchScore")

            if score:
                print("\nMatch:", info.get("team1", {}).get("teamName"),
                      "vs", info.get("team2", {}).get("teamName"))
                print("Match state:", info.get("state"))
                print("Score data:", score)
