import requests


LEAGUES = {
    "NBA": ("basketball", "nba"),
    "NFL": ("football", "nfl"),
    "MLB": ("baseball", "mlb"),
    "NHL": ("hockey", "nhl"),
    "NCAA": ("football", "college-football"),
    "NCAAM": ("basketball", "mens-college-basketball"),
    "NCAA Baseball": ("baseball", "college-baseball"),
}


def get_scores(league_name):
    sport, league = LEAGUES[league_name]

    url = (
        f"https://site.api.espn.com/apis/site/v2/"
        f"sports/{sport}/{league}/scoreboard"
    )

    params = {
        "limit": 100
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    games = []

    for event in data.get("events", []):
        competition = event["competitions"][0]

        home = None
        away = None

        for competitor in competition["competitors"]:
            if competitor["homeAway"] == "home":
                home = competitor

            elif competitor["homeAway"] == "away":
                away = competitor

        if home is None or away is None:
            continue

        home_team = home["team"]
        away_team = away["team"]

        game = {
            "league": league_name,
            "id": event["id"],

            "home_team": home_team.get(
                "displayName",
                "Unknown"
            ),

            "away_team": away_team.get(
                "displayName",
                "Unknown"
            ),

            "home_abbr": home_team.get(
                "abbreviation",
                ""
            ),

            "away_abbr": away_team.get(
                "abbreviation",
                ""
            ),

            "home_score": home.get(
                "score",
                "0"
            ),

            "away_score": away.get(
                "score",
                "0"
            ),

            "home_logo": home_team.get("logo"),
            "away_logo": away_team.get("logo"),

            "status": competition["status"]["type"].get(
                "description",
                ""
            ),

            "detail": competition["status"]["type"].get(
                "detail",
                ""
            ),

            "date": event.get(
                "date",
                ""
            )
        }

        games.append(game)

    return games