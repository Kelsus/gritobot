#!/bin/bash

# Ensure the environment variables are set
if [ -z "$SLACK_TOKEN" ]; then
    echo "SLACK_TOKEN environment variable is not set!"
    exit 1
fi

# Deploy using SAM without needing to use --parameter-overrides explicitly
sam.cmd deploy --parameter-overrides SlackToken=$SLACK_TOKEN OpenAIAPIKey=$OPENAI_API_KEY
