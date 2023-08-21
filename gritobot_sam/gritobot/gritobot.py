import json
import boto3

# AWS Lambda Client
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Parse the incoming request
    print(event['event'])

    # URL Verification Challenge
    if "challenge" in event['event']:
        return {
            'statusCode': 200,
            'body': event["event"]["challenge"],
            'headers': {
                'Content-Type': 'text/plain',
            }
        }
    # Process incoming Slack events
    else:
        if event['event']['type'] == 'app_mention':
            # Acknowledge receipt of the event
            # Then invoke the second Lambda function asynchronously
            lambda_client.invoke(
                FunctionName='ProcessGritoBot',
                InvocationType='Event',
                Payload=json.dumps(event)
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