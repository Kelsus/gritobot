# gritobot_sam

This project contains source code and supporting files for a serverless application that is the back end for a slack chatbot that uses GPT-4 to generate responses.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.


## Build and deploy the application
This application relies on soeme environment variables that contains secrets, so you need to set them somehow in your local environment (I used direnv so they would get set while entering the development project directory.)

These are the env vars you need:
```bash
export SLACK_TOKEN=*your slack token*
export OPENAI_API_KEY=*your openai api key*
```

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided --parameter-overrides SlackToken=$SLACK_TOKEN OpenAIAPIKey=$OPENAI_API_KEY
```

Once you have built the application once, you can then use the deploy.sh script for further deploys. It will make use of the config file that the guided deployment makes and save you from having to always fill in teh --parameter-overrides flags to deploy the app which is too much typing.

The build command will build the source of your application. The deploy command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

This app also requires that you create and install a Slack app with bot capabilities that will send app_mention events to the API GATEWAY endpoint created in this app. Here are general instructions for how to do that.

# Creating a Slack App with Mention Responses

Follow these steps to create a Slack app that responds when it's mentioned in a channel:

## 1. Setting up the Slack App

### 1.1. Create a New App

- Navigate to [Slack's App Page](https://api.slack.com/apps)
- Click "Create New App".
- Name your app and select your workspace from the dropdown.
- Click "Create App".

### 1.2. Bot Token Scopes

- Go to the "OAuth & Permissions" section and scroll down to "Scopes".
- Add the following scopes:
  - `app_mentions:read` - This allows your app to get notifications when it's mentioned.
  - `chat:write` - This allows the bot to send messages back to the channel.
- Note: Add other scopes as necessary for additional functionality.

### 1.3. Event Subscriptions

- Click on "Event Subscriptions" in the left sidebar.
- Toggle on "Enable Events".
- Enter your API Gateway endpoint URL in the "Request URL" field.
- After Slack verifies the URL, expand "Subscribe to bot events" and add the `app_mention` event.

### 1.4. Interactive Components (Optional)

- Go to "Interactive Components" in the sidebar.
- Toggle it on.
- Enter your API Gateway endpoint URL (or another endpoint if handling interactive actions differently) in the "Request URL" field.

### 1.5. Install App

- Go back to the main page for your app.
- Click "Install App to Workspace".
- Follow the prompts to authorize the app in your Slack workspace. Once completed, Slack will provide you with an OAuth token. Store this safely; you'll need it to authenticate API calls from your service.

## 2. Listening for Events & Responding

### 2.1. Listen for app_mention Events

- When your endpoint receives a POST request from Slack, check the event type. For an app mention, it will be `app_mention`.

### 2.2. Extracting Information

- From the POST request body, you can extract the channel ID (`event.channel`), user ID of the person who mentioned the bot (`event.user`), and the text of the message (`event.text`).

### 2.3. Responding to the Mention

To send a response when the bot is mentioned:

1. Utilize Slack's `chat.postMessage` method.
2. Send a POST request to `https://slack.com/api/chat.postMessage`.

   **Headers:**
   ```
   Authorization: Bearer YOUR_OAUTH_TOKEN
   Content-Type: application/json
   ```
   
   **Body:**
   ```json
   {
       "channel": CHANNEL_ID,
       "text": "Your response message here"
   }
   ```

## 3. Refining and Testing

### 3.1. Invite Bot to Channel

- To utilize the bot within a channel, you must invite it. Use the command: `/invite @YourBotName`.

### 3.2. Testing

- Test the bot by mentioning it in a message, for example, `@YourBotName how are you?`. If correctly set up, your bot should respond appropriately.

**Note**: Libraries and SDKs for various programming languages are available, which can help simplify the process of processing events and communicating with Slack. For comprehensive and up-to-date information, always refer to Slack's official API documentation.

