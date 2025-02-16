from groq import Groq
import os
from dotenv import load_dotenv
import json
from tools import AVAILABLE_FUNCTIONS, TOOLS

load_dotenv()

client = Groq(api_key = os.getenv('GROQ_API_KEY'))
MODEL = 'llama3-70b-8192'


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
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="required",  
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
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