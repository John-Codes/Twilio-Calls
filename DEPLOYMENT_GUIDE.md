# Deployment Guide for Twilio Call Routing App on Back4App

This guide provides step-by-step instructions for deploying the Twilio call routing application to Back4App, configuring it to handle inbound calls, and testing the functionality with real phone numbers. Back4App primarily supports Parse Server and cloud code, so this guide focuses on deploying the Flask app as cloud code or a custom solution.

## Prerequisites

- **Back4App Account**: Ensure you have an account and a Parse app created on Back4App.
- **Twilio Account**: You need a Twilio account with a phone number configured for inbound calls.
- **Environment Variables**: Ensure you have the necessary Twilio credentials and phone numbers set up in a `.env` file or ready to be configured in Back4App.

## Step 1: Prepare the Application

The application consists of:
- `incoming_call_router.py`: Flask app for handling Twilio webhooks.
- `daily_assigner.py`: Logic for assigning a person based on the day of the week.
- `requirements.txt`: List of Python dependencies.

Ensure error handling and verbose logging are implemented in the code (already added in the latest updates).

## Step 2: Deploying to Back4App

Back4App may not directly support running a standalone Flask app with Docker containers outside of Parse Server. Instead, you can deploy the app logic as **Cloud Code** or explore custom deployment options if available.

### Option 1: Deploy as Cloud Code

1. **Access Cloud Code in Back4App**:
   - Log in to your Back4App dashboard.
   - Navigate to your Parse app.
   - Go to the "Server Settings" or "Cloud Code" section.

2. **Adapt Flask App to Cloud Code**:
   - Back4App Cloud Code typically uses Node.js, but you can integrate Python scripts or use a custom endpoint.
   - Convert the Flask app logic into a Parse Cloud Function or host the Flask app externally if Back4App supports custom endpoints.
   - Alternatively, rewrite the core routing logic (`incoming_call_router.py` and `daily_assigner.py`) as a Parse Cloud Function in JavaScript if Python support is limited.

3. **Upload Code**:
   - If Python is supported, upload the necessary files (`incoming_call_router.py`, `daily_assigner.py`, `requirements.txt`) to the Cloud Code directory.
   - Install dependencies if Back4App allows Python package installation (e.g., via `pip` or a custom setup script).

4. **Configure Environment Variables**:
   - In Back4App, go to "App Settings" > "Environment Variables".
   - Add the following variables from your `.env` file:
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_FROM_NUMBER`
     - Phone numbers for each person (e.g., `EDWARD`, `JOHNNY_R`, etc.).
   - Ensure these are securely stored and not hardcoded in the code.

5. **Set Up Webhook Endpoint**:
   - Back4App will provide a URL for your Cloud Code function or custom endpoint (e.g., `https://your-app-name.parseapp.com/voice`).
   - Configure this URL in Twilio as the webhook for inbound calls (see Step 3).

### Option 2: Custom Deployment (if supported)

If Back4App allows custom container deployment or external hosting:
1. Build the Docker image locally using the provided `Dockerfile`:
   ```bash
   docker build -t twilio-call-router .
   ```
2. Push the image to a container registry (e.g., Docker Hub) or deploy directly if Back4App supports custom containers.
3. Follow Back4App's documentation for deploying custom apps or containers.

## Step 3: Configure Twilio Webhook

1. Log in to your Twilio Console.
2. Navigate to "Phone Numbers" > "Manage" > Select your Twilio number.
3. Under "Voice & Fax", set the webhook URL for incoming calls to the Back4App endpoint (e.g., `https://your-app-name.parseapp.com/voice`).
4. Ensure the HTTP method is set to `POST`.

## Step 4: Test Inbound Calls

1. **Make Test Calls**:
   - Use a real phone number to call your Twilio number.
   - Verify that the call is routed to the correct person based on the day of the week as defined in `daily_assigner.py`.

2. **Monitor Logs**:
   - Access logs in Back4App under "Logs" or "Cloud Code Logs" in the dashboard.
   - Check for verbose error messages or success logs to confirm the app is processing calls correctly.
   - Look for entries like:
     - `Processing incoming call, fetching assigned person for today.`
     - `Incoming call on [Day], forwarding to [Name] at [Number]`
     - Any error messages if something fails.

3. **Debug Issues**:
   - If calls are not routing correctly, review the logs for errors related to Twilio API, environment variables, or assignment logic.
   - Adjust the code or configuration as needed and redeploy.

## Step 5: Finalize Deployment

- Once testing confirms that inbound calls are routed correctly, ensure all environment variables are securely set in Back4App.
- Document any specific configurations or troubleshooting steps for future reference.
- Monitor the app periodically via Back4App logs to ensure ongoing functionality.

## Troubleshooting

- **Webhook Not Triggering**: Verify the webhook URL in Twilio matches the Back4App endpoint and is accessible (test with a tool like Postman if needed).
- **Environment Variables Missing**: Double-check that all required variables are set in Back4App.
- **Routing Errors**: Check logs for issues with `daily_assigner.py` logic or phone number retrieval.
- **Twilio Errors**: Ensure your Twilio account has sufficient credits and the phone number is active for inbound calls.

If Back4App's limitations prevent direct deployment of the Flask app, consider alternative hosting platforms like Heroku, AWS Lambda with API Gateway, or a VPS for full control over the environment.

For further assistance, refer to Back4App documentation (https://www.back4app.com/docs) or Twilio support (https://support.twilio.com).
