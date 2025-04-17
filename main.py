import streamlit as st
from data.mlb import get_today_games, get_starting_pitchers, get_batters_for_game, get_player_stats, get_weather, get_park_factor
from ai.projection import project_hr_projection

st.set_page_config(page_title="MLB AI HR Prop Bot", layout="wide")
st.title("⚾ MLB Daily AI Home Run Prop Bot")

games = get_today_games()
projections = []

for game in games:
    game_id = game["gamePk"]
    venue = game["venue"]
    home_team = game["home_team"]
    away_team = game["away_team"]

    pitchers = get_starting_pitchers(game_id)
    weather = get_weather(venue)
    park_factor = get_park_factor(venue)

    batters = get_batters_for_game(game_id)

    for player in batters:
        stats = get_player_stats(player["id"])
        projection = project_hr_projection(stats, park_factor, weather)

        projections.append({
            "Player": player["name"],
            "Team": player["team"],
            "Opponent": f"{away_team} @ {home_team}",
            "Ballpark": venue,
            "Projected HR": projection["projected_hr"],
            "Confidence": projection["confidence"],
            "Pick": projection["pick"]
        })

st.dataframe(projections, use_container_width=True)
# main.py with auto-loaded batters - full logic was prepared earlier
