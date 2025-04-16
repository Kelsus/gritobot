#!/bin/bash

# Load environment variables from .env file
if [ -f "../.env" ]; then
    echo "Loading environment variables from ../.env"
    export $(grep -v '^#' "../.env" | xargs)
else
    echo "No ../.env file found!"
fi

# Ensure the environment variables are set
if [ -z "$SLACK_TOKEN" ]; then
    echo "SLACK_TOKEN environment variable is not set!"
    exit 1
fi

if [ -z "$OPENAI_API_TOKEN" ]; then
    echo "OPENAI_API_TOKEN environment variable is not set!"
    exit 1
fi

# Set default region if not already set
if [ -z "$AWS_REGION" ]; then
    AWS_REGION="us-east-1"  # Change this to your preferred region
    echo "AWS_REGION not set, using default: $AWS_REGION"
fi

# Set the AWS profile to use
AWS_PROFILE="AdministratorAccess-160605163512"
echo "Using AWS profile: $AWS_PROFILE"

# Check if AWS SSO session is active
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity --profile $AWS_PROFILE &>/dev/null; then
    echo "No active AWS session found. Logging in with SSO..."
    if ! aws sso login --profile $AWS_PROFILE; then
        echo "AWS SSO login failed. Please check your AWS configuration."
        echo "Make sure you have:"
        echo "1. AWS CLI v2 installed"
        echo "2. Configured SSO with 'aws configure sso'"
        echo "3. Correct AWS profile in ~/.aws/config"
        exit 1
    fi
fi

# Verify credentials after login
if ! aws sts get-caller-identity --profile $AWS_PROFILE &>/dev/null; then
    echo "Failed to obtain AWS credentials even after SSO login."
    exit 1
fi

echo "AWS credentials verified successfully."

# Deploy using SAM with region and parameter overrides
echo "Starting SAM deployment..."
sam deploy \
    --region $AWS_REGION \
    --resolve-s3 \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        SlackToken=$SLACK_TOKEN \
        OpenAIAPIKey=$OPENAI_API_TOKEN \
    --profile $AWS_PROFILE
