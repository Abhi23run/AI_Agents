from groq import Groq
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

client = Groq(api_key = os.getenv('GROQ_API_KEY'))
MODEL = 'llama3-70b-8192'

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

def run_conversation(user_prompt):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": "You are a function calling LLM that understands the incoming user question and calls the relevant functions depending on the question. \
            Make sure to use the Linkedin API when asked about any company."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
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
                            "description": "The name of the NBA team (e.g. 'Golden State Warriors')",
                        }
                    },
                    "required": ["team_name"],
                },
            },
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
                "required": ["company_name"],
            },
        }
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="required",  
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_game_score": get_game_score, "get_company_details" : get_company_details
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                **function_args
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content

# user_prompt = "What was the score of the Nuggets game and also the warriors game?"
# print(run_conversation(user_prompt))