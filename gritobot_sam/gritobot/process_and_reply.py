import os
import re
import json
from slack_sdk import WebClient

import openai

async def handle_app_mentions(body):
    print("HI JC!!! we got into the handler")
    user = body["user"]
    text = body["text"]

    # Call GPT-4 API
    prompt = f"Generate a funny and irreverent response to the following message: {text}"
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=50, n=1, stop=None, temperature=0.7)

    # Extract the generated response
    generated_response = response.choices[0].text.strip()
    print("HI JC!!! here's generated_response: ", generated_response)

    # Respond to the user
    say(f"{generated_response}")


def process_and_reply(event, context):
    # Parse the incoming request
    body = event['event']

    # Only process "app_mention" events
    if body.get('type') == 'app_mention':
        asyncio.run(handle_app_mentions(body))