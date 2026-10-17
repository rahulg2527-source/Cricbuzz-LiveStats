
from app.api.cricbuzz_api import get_live_matches

matches = get_live_matches()

live_matches = []

for match in matches:
    state = match["state"].strip().lower()

    if state == "in progress":
        live_matches.append(match)

print("Total matches:", len(matches))
print("In-progress matches:", len(live_matches))

for match in live_matches:
    print(
        match["team1"],
        "vs",
        match["team2"],
        "|",
        match["status"],
    )
