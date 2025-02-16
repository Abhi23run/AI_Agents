import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_company_details(company_name):
    """Fetch company details from LinkedIn API"""
    url = "https://linkedin-data-api.p.rapidapi.com/get-company-details"
    headers = {
        "x-rapidapi-key": os.getenv('x-rapidapi-key'),
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
    }
    querystring = {"username": company_name}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_json = response.json()
        return json.dumps(response_json.get("data", {}))  # Return only "data" field
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code})


def get_game_score(team_name):
    """Get the current score for a given NBA game by querying the Flask API."""
    url = f'http://127.0.0.1:5000/score?team={team_name}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code})

# Automatically register all functions that start with "get_"
AVAILABLE_FUNCTIONS = {name: func for name, func in globals().items() if callable(func) and name.startswith("get_")}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_game_score",
            "description": "Get the score for a given NBA game",
            "parameters": {
                "type": "object",
                "properties": {
                    "team_name": {
                        "type": "string",
                        "description": "The name of the NBA team (e.g. 'Golden State Warriors')"
                    }
                },
                "required": ["team_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_details",
            "description": "Fetch company details from LinkedIn API using the company username.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The LinkedIn username of the company (e.g. 'Vanguard')."
                    }
                },
                "required": ["company_name"]
            }
        }
    }
]

if __name__ == "__main__":
    print(AVAILABLE_FUNCTIONS.keys())  # Should print: dict_keys(['get_company_details', 'get_game_score'])
