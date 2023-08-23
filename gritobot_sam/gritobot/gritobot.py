import json
import boto3
import os

# AWS Lambda Client
lambda_client = boto3.client('lambda')

PROCESS_AND_REPLY_FUNCTION = os.environ["PROCESS_AND_REPLY_FUNCTION"]


def lambda_handler(event, context):
    # Parse the incoming request
    print("Incoming event:")
    print(event)

    # Check if body exists and is a string, then parse it
    body = json.loads(event["body"]) if "body" in event and isinstance(event["body"], str) else {}

    # URL Verification Challenge
    if "challenge" in body:
        return {
            'statusCode': 200,
            'body': body["challenge"],
            'headers': {
                'Content-Type': 'text/plain',
            }
        }
    # Process incoming Slack events
    else:
        if body.get('event', {}).get('type') == 'app_mention':
            # Acknowledge receipt of the event
            # Then invoke the second Lambda function asynchronously
            lambda_client.invoke(
                FunctionName=PROCESS_AND_REPLY_FUNCTION,
                InvocationType='Event',
                Payload=json.dumps(body)  # Also, ensure you pass the payload as a string
            )
            return {
                'statusCode': 200,
                'body': "Event received",
                'headers': {
                    'Content-Type': 'application/json',
                }
            }
        else:
            return {
                'statusCode': 200,
                'body': "No 'app_mention' event in the request.",
                'headers': {
                'Content-Type': 'text/plain',
                }
            }
