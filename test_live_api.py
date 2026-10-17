
import os
import sys

import requests
from dotenv import load_dotenv

# Load API credentials from the local .env file
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "cricbuzz-cricket.p.rapidapi.com"
API_URL = f"https://{API_HOST}/matches/v1/live"
def main():
    if not API_KEY or API_KEY == "PASTE_YOUR_NEW_KEY_HERE":
        print("ERROR: RAPIDAPI_KEY is missing or is still a placeholder.")
        print("Check your local .env file.")
        sys.exit(1)

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST,
    }

    print("Testing Cricbuzz Live Matches API...")
    print("Endpoint:", API_URL)

    try:
        response = requests.get(
            API_URL,
            headers=headers,
            timeout=20,
        )

        print("HTTP status:", response.status_code)

        if not response.ok:
            print("API request was rejected.")
            print("Response details:")

            # Show the server's error message, never the API key.
            # Avoid printing request headers or the complete request object.
            print(response.text[:500])
            print(
                "\nCheck the API key, subscription status, "
                "endpoint access, and rate limits."
            )
            return

        try:
            data = response.json()
        except ValueError:
            print("ERROR: The server returned a non-JSON response.")
            print("Response preview:", response.text[:300])
            return

        if not isinstance(data, dict):
            print("ERROR: Unexpected response format.")
            print("Expected a JSON object.")
            return

        match_count = 0
        match_summaries = []

        for match_type in data.get("typeMatches", []):
            if not isinstance(match_type, dict):
                continue

            for series in match_type.get("seriesMatches", []):
                if not isinstance(series, dict):
                    continue

                wrapper = series.get("seriesAdWrapper", {})
                if not isinstance(wrapper, dict):
                    continue

                matches = wrapper.get("matches", [])
                if not isinstance(matches, list):
                    continue

                for match in matches:
                    if not isinstance(match, dict):
                        continue

                    info = match.get("matchInfo", {})
                    if not isinstance(info, dict):
                        continue

                    match_count += 1

                    team1 = info.get("team1", {}).get("teamName", "Team 1")
                    team2 = info.get("team2", {}).get("teamName", "Team 2")
                    status = info.get("status", "Status unavailable")
                    state = info.get("state", "Unknown")

                    match_summaries.append(
                        f"{team1} vs {team2} | {state} | {status}"
                    )

        print("Response is valid JSON: True")
        print("Top-level fields:", ", ".join(data.keys()))
        print("Matches found:", match_count)

        if match_summaries:
            print("\nSample matches (up to 5):")
            for summary in match_summaries[:5]:
                print("-", summary)
        else:
            print(
                "No matches were found in the expected "
                "typeMatches/seriesMatches structure."
            )

    except requests.Timeout:
        print("ERROR: The API request timed out.")
    except requests.ConnectionError:
        print("ERROR: Could not connect to the API.")
    except requests.RequestException as error:
        print("ERROR: Request failed:", type(error).__name__)


if __name__ == "__main__":
    main()
