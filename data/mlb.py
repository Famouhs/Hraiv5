import requests
from datetime import datetime

def get_today_games():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
    response = requests.get(url)
    games = []
    for date in response.json().get("dates", []):
        for game in date["games"]:
            games.append({
                "gamePk": game["gamePk"],
                "home_team": game["teams"]["home"]["team"]["name"],
                "away_team": game["teams"]["away"]["team"]["name"],
                "venue": game["venue"]["name"]
            })
    return games

def get_starting_pitchers(game_id):
    try:
        url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
        response = requests.get(url).json()
        home_id = response["teams"]["home"]["pitchers"][0]
        away_id = response["teams"]["away"]["pitchers"][0]
        home_name = response["teams"]["home"]["players"][f"ID{home_id}"]["person"]["fullName"]
        away_name = response["teams"]["away"]["players"][f"ID{away_id}"]["person"]["fullName"]
        return {"home_pitcher": home_name, "away_pitcher": away_name}
    except:
        return {}

def get_batters_for_game(game_id):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    response = requests.get(url).json()
    batters = []
    for team_key in ["home", "away"]:
        players = response["teams"][team_key]["players"]
        for player_id, data in players.items():
            pos = data.get("position", {}).get("code", "")
            if pos in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "D"]:  # Batters only
                batters.append({
                    "id": data["person"]["id"],
                    "name": data["person"]["fullName"],
                    "team": response["teams"][team_key]["team"]["name"]
                })
    return batters

def get_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season,gameLog&group=hitting"
    response = requests.get(url).json()
    stats = {"season_hr": 0, "season_games": 0, "recent_hr": 0, "recent_games": 0}
    try:
        season = response["stats"][0]["splits"][0]["stat"]
        stats["season_hr"] = int(season.get("homeRuns", 0))
        stats["season_games"] = int(season.get("gamesPlayed", 1))
        recent_games = response["stats"][1]["splits"][:5]
        stats["recent_games"] = len(recent_games)
        stats["recent_hr"] = sum(int(g["stat"].get("homeRuns", 0)) for g in recent_games)
    except:
        pass
    return stats

def get_weather(venue_name):
    return {"temp_f": 75, "wind_mph": 8, "wind_dir": "S"}

def get_park_factor(venue_name):
    park_factors = {
        "Coors Field": 1.25,
        "Yankee Stadium": 1.17,
        "Petco Park": 0.85,
        "Fenway Park": 1.08
    }
    return park_factors.get(venue_name, 1.00)
# data/mlb.py with get_today_games, get_starting_pitchers, get_player_stats, get_weather, get_park_factor
