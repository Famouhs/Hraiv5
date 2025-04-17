def project_hr_projection(stats, park_factor=1.0, weather=None):
    season_rate = stats["season_hr"] / max(stats["season_games"], 1)
    recent_rate = stats["recent_hr"] / max(stats["recent_games"], 1)
    hr_rate = 0.6 * recent_rate + 0.4 * season_rate

    weather_boost = 0
    if weather:
        if weather.get("temp_f", 70) > 75:
            weather_boost += 0.03
        if weather.get("wind_dir") in ["S", "SE", "E"]:
            if weather.get("wind_mph", 0) >= 10:
                weather_boost += 0.03

    proj = hr_rate * park_factor * (1 + weather_boost)
    confidence = round(min(max((proj - 0.5) * 200, 0), 100))

    return {
        "projected_hr": round(proj, 3),
        "confidence": f"{confidence}%",
        "pick": "Over 0.5 HR" if proj >= 0.5 else "Under 0.5 HR"
    }
# ai/projection.py with project_hr_projection using real stats and weather
