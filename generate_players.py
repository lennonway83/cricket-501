import requests
import json

API_KEY = "fIGbQ0vXikWEdVvYaoK5TjB9PSEEJRu9boc0AhqoHuNTrkZpRs7gM5RLoxWx"

all_players = []

# Fetch first page of players (SportMonks paginates results)
response = requests.get(f"https://cricket.sportmonks.com/api/v2.0/players?api_token={API_KEY}&page=1")
players = response.json()['data']

for p in players:
    player_id = p['id']
    
    # Fetch career stats for each player
    career_response = requests.get(f"https://cricket.sportmonks.com/api/v2.0/players/{player_id}/career?api_token={API_KEY}")
    career = career_response.json()['data']
    
    all_players.append({
        "name": p['fullname'],
        "odi_runs": career.get("odi_runs", 0),
        "test_runs": career.get("test_runs", 0),
        "t20i_runs": career.get("t20i_runs", 0),
        "highest_score": career.get("highest_score", 0),
        "odi_wickets": career.get("odi_wickets", 0),
        "test_wickets": career.get("test_wickets", 0),
        "t20i_wickets": career.get("t20i_wickets", 0)
    })

# Save to players.json
with open('players.json', 'w') as f:
    json.dump(all_players, f, indent=2)

print("players.json generated successfully!")
