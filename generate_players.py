import requests
import json

API_KEY = "fIGbQ0vXikWEdVvYaoK5TjB9PSEEJRu9boc0AhqoHuNTrkZpRs7gM5RLoxWx"

all_players = []
page = 1
has_more = True

while has_more:
    print(f"Fetching page {page} of players...")
    response = requests.get(
        f"https://cricket.sportmonks.com/api/v2.0/players?api_token={API_KEY}&page={page}"
    )
    data = response.json()
    players = data.get('data', [])
    
    if not players:
        has_more = False
        break

    for p in players:
        player_id = p['id']
        
        # Fetch career stats for each player
        career_response = requests.get(
            f"https://cricket.sportmonks.com/api/v2.0/players/{player_id}/career?api_token={API_KEY}"
        )
        career = career_response.json().get('data', {})

        all_players.append({
            "name": p.get('fullname', 'Unknown'),
            "odi_runs": career.get("odi_runs", 0),
            "test_runs": career.get("test_runs", 0),
            "t20i_runs": career.get("t20i_runs", 0),
            "highest_score": career.get("highest_score", 0),
            "odi_wickets": career.get("odi_wickets", 0),
            "test_wickets": career.get("test_wickets", 0),
            "t20i_wickets": career.get("t20i_wickets", 0)
        })

    # Check if there's a next page
    meta = data.get('meta', {})
    current_page = meta.get('current_page', page)
    last_page = meta.get('last_page', page)
    page += 1
    if current_page >= last_page:
        has_more = False

# Save JSON
with open('players.json', 'w') as f:
    json.dump(all_players, f, indent=2)

print(f"Done! {len(all_players)} players saved to players.json")
