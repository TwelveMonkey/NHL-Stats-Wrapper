import requests
import urllib

BASE_URL = "https://statsapi.web.nhl.com/api/v1/"


def get_request(url_suffix: str, query_modifier: str = "") -> dict:
    try:
        print(f"GET -- {url_suffix}{query_modifier}")
        response = requests.request(
            "GET", url=f"{BASE_URL}{url_suffix}{query_modifier}"
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(
            f"An error occured with your request {BASE_URL}{url_suffix}{query_modifier}------{e}"
        )
    return response.json()


def encode_modifier(query: dict) -> str:
    return urllib.parse.urlencode(query)


team_dict = {
    "New Jersey Devils": 1,
    "New York Islanders": 2,
    "New York Rangers": 3,
    "Philadelphia Flyers": 4,
    "Pittsburgh Penguins": 5,
    "Boston Bruins": 6,
    "Buffalo Sabres": 7,
    "Montreal Canadiens": 8,
    "Ottawa Senators": 9,
    "Toronto Maple Leafs": 10,
    "Carolina Hurricanes": 12,
    "Florida Panthers": 13,
    "Tampa Bay Lightning": 14,
    "Washington Capitals": 15,
    "Chicago Blackhawks": 16,
    "Detroit Red Wings": 17,
    "Nashville Predators": 18,
    "St. Louis Blues": 19,
    "Calgary Flames": 20,
    "Colorado Avalanche": 21,
    "Edmonton Oilers": 22,
    "Vancouver Canucks": 23,
    "Anaheim Ducks": 24,
    "Dallas Stars": 25,
    "Los Angeles Kings": 26,
    "San Jose Sharks": 28,
    "Columbus Blue Jackets": 29,
    "Minnesota Wild": 30,
    "Winnipeg Jets": 52,
    "Arizona Coyotes": 53,
    "Vegas Golden Knights": 54,
}
