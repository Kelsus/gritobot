import os
import json
from slack_sdk import WebClient
import openai

# OpenAI API initialization
openai.api_key = os.environ["OPENAI_API_KEY"]

# Slack client
slack_token = os.environ["SLACK_TOKEN"]
client = WebClient(token=slack_token)

# Global variable to store bot user ID
BOT_USER_ID = None

def get_bot_user_id():
    global BOT_USER_ID
    
    # If BOT_USER_ID hasn't been cached, fetch it
    if not BOT_USER_ID:
        response = client.auth_test()
        BOT_USER_ID = response["user_id"]
    
    return BOT_USER_ID


def get_channel_history(channel, limit=25):
    """
    Fetch latest messages from Slack channel.
    
    Args:
    - channel (str): Channel ID.
    - limit (int): Number of latest messages to fetch.
    
    Returns:
    - List of messages.
    """
    history = client.conversations_history(channel=channel, limit=limit)
    return history['messages']

def get_thread_history(channel, thread_ts, limit=25):
    """
    Fetch messages from a Slack thread.
    
    Args:
    - channel (str): Channel ID.
    - thread_ts (str): Timestamp of the parent message of the thread.
    - limit (int): Number of latest messages to fetch.
    
    Returns:
    - List of thread messages.
    """
    thread = client.conversations_replies(channel=channel, ts=thread_ts, limit=limit)
    return thread['messages']

def handle_app_mentions(body):
    print("Processing app mention...")

    user = body["user"]
    text = body["text"]
    thread_ts = body.get("thread_ts", None)  # Get the thread_ts if it exists, otherwise None

    # Fetch history depending on if it's in a thread or not
    if thread_ts:
        history = get_thread_history(body["channel"], thread_ts)
    else:
        history = get_channel_history(body["channel"])
        history = reversed(history)  # Only reverse for channel history, not for thread history
    
    # Fetch bot user ID
    bot_user_id = get_bot_user_id()

    # Initial system instruction for GPT-4
    messages = [
        {"role": "system", "content": f"You are a sarcastic, nihilistic, irreverent robot named Gritobot that makes fun of whatever anyone says to you sort of like Daria Morgendorffer or Deadpool/Wade Wilson. You don't pull punches. In your responses you can refer to the user as <@{user}>. Your resopnses should be short and quippy, about the length of a tweet unless the context of the conversation requires you to say something longer."},
    ]
    
    # Add historical messages to the messages list
    for message in history:
        if 'user' in message and 'text' in message:
            if message['user'] == bot_user_id:
                role= "system"
                messageText = message['text']
            else: 
                role = "user"
                messageText = f"<@{user}> wrote: {message['text']}>"

            messages.append({"role": role, "content": messageText})
    
    # Add the recent message
    messages.append({"role": "user", "content": f"<@{user}> wrote: {message['text']}>"})

    print("Messages for GPT API:")
    print(messages)
    
    # Call GPT-4 Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    # Extract the generated response
    generated_response = response['choices'][0]['message']['content']

    # Respond to the user
    say(body["channel"], generated_response, thread_ts)


def say(channel, message, thread_ts=None):
    # Send a message to Slack
    client.chat_postMessage(channel=channel, text=message, thread_ts=thread_ts)  # Add thread_ts param when replying inside a thread


def process_and_reply(event, context):
    # Parse the incoming request
    body = event['event']

    # Only process "app_mention" events
    if body.get('type') == 'app_mention':
        handle_app_mentions(body)