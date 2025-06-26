# Set up Twilio Call Routing
https://www.twilio.com/docs/voice/tutorials/how-to-respond-to-incoming-phone-calls/python 


# Deployment Guide for Twilio Call Routing App Using Docker

This guide provides step-by-step instructions for deploying the Twilio call routing application using a Docker image on any server. It includes configuring the app to handle inbound calls via Twilio webhooks and testing the functionality with real phone numbers. The application is built with Python, and this guide focuses on containerizing it for deployment flexibility.

## Prerequisites

- **Twilio Account**: Ensure you have a Twilio account with a phone number configured for inbound calls.
- **Docker**: Install Docker on your local machine for building the image and on the target server for deployment (or use a container registry like Docker Hub).
- **Server Access**: You need access to a server (e.g., VPS, cloud instance like AWS EC2, Google Cloud, or Azure) with Docker installed, or the ability to deploy Docker containers.
- **Environment Variables**: Have your Twilio credentials and phone numbers ready for configuration, typically stored in a `.env` file or set directly on the server.

## Step 1: Prepare the Application

The application consists of:
- `incoming_call_router.py`: Flask app for handling Twilio webhooks.
- `daily_assigner.py`: Logic for assigning a person based on the day of the week.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Instructions for building the Docker image.

Ensure error handling and verbose logging are implemented in the code (already included in the latest updates). Verify that all necessary files are in your project directory before proceeding.

## Step 2: Build the Docker Image

1. **Build the Image Locally**:
   Open a terminal in your project directory (where the `Dockerfile` is located) and run:
   ```bash
   docker build -t twilio-call-router .
   ```
   This builds a Docker image named `twilio-call-router` based on the provided `Dockerfile`.

2. **Test the Image Build Locally (Optional)**:
   To ensure the build process completed successfully, you can run a container locally, but note that full API testing requires Twilio webhooks to be set up on a server with a static IP:
   ```bash
   docker run -p 5000:5000 --env-file .env twilio-call-router
   ```
   Local testing of the full API without Twilio webhooks is not practical. Use this step only to verify the container starts without errors.
   

3. **Push to a Container Registry (Optional)**:
   If your server cannot build the image directly, push it to a registry like Docker Hub for easy access:
   - Log in to Docker Hub:
     ```bash
     docker login
     ```
   - Tag the image:
     ```bash
     docker tag twilio-call-router yourusername/twilio-call-router:latest
     ```
   - Push the image:
     ```bash
     docker push yourusername/twilio-call-router:latest
     ```

## Step 3: Deploy the Docker Container to a Server

1. **Set Up the Server**:
   - Ensure Docker is installed on your target server. If not, install it following the official Docker documentation for your server's OS (e.g., Ubuntu, CentOS, or Windows Server).
   - Securely access your server via SSH or another method.

2. **Transfer the Image or Pull from Registry**:
   - If you pushed the image to a registry, pull it on the server:
     ```bash
     docker pull yourusername/twilio-call-router:latest
     ```
   - Alternatively, if the image is built locally and the server is accessible, you can save and transfer it:
     ```bash
     # On local machine
     docker save -o twilio-call-router.tar twilio-call-router
     scp twilio-call-router.tar user@server-ip:/path/to/save
     # On server
     docker load -i /path/to/save/twilio-call-router.tar
     ```

3. **Run the Container**:
   - Configure environment variables either via a `.env` file or directly in the command. If using a `.env` file, ensure it’s on the server in the working directory.
   - Start the container, mapping the app’s port (default 5000) to a port on the server:
     ```bash
     docker run -d -p 5000:5000 --env-file .env --name twilio-router twilio-call-router
     ```
   - If not using a `.env` file, set variables manually (replace `<value>` with actual values):
     ```bash
     docker run -d -p 5000:5000 --name twilio-router \
       -e TWILIO_ACCOUNT_SID=<value> \
       -e TWILIO_AUTH_TOKEN=<value> \
       -e TWILIO_FROM_NUMBER=<value> \
       -e EDWARD=<value> \
       -e JOHNNY_R=<value> \
       # Add other phone numbers as needed
       twilio-call-router
     ```
   - Verify the container is running:
     ```bash
     docker ps
     ```

4. **Ensure Accessibility with a Static IP**:
   - Ensure your server has a static IP address for reliable Twilio webhook functionality. Twilio requires a consistent, publicly accessible endpoint, which is not possible with dynamic IPs that may change.
   - If the server has a firewall, open the port (e.g., 5000):
     ```bash
     # Example for Ubuntu with ufw
     sudo ufw allow 5000/tcp
     ```
   - If using a cloud provider, ensure the port is open in the security group or network settings.
   - Determine the server’s static public IP or domain name to form the webhook URL (e.g., `http://your-server-ip:5000/voice` or `http://your-domain.com:5000/voice`).

5. **Optional: Use a Reverse Proxy (Recommended for Production)**:
   - For better security and management, set up a reverse proxy like Nginx or Traefik to forward requests to the container. This allows using standard ports (80 or 443) and SSL/TLS for HTTPS.
   - Example Nginx configuration:
     ```
     server {
         listen 80;
         server_name your-domain.com;

         location /voice {
             proxy_pass http://localhost:5000/voice;
             proxy_http_version 1.1;
             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection "upgrade";
             proxy_set_header Host $host;
         }
     }
     ```
   - Enable HTTPS with a tool like Certbot for Let’s Encrypt certificates.

## Step 4: Configure Twilio Webhook

1. **Determine the Public Endpoint**:
   - Use the server’s public IP or domain to form the webhook URL (e.g., `http://your-server-ip:5000/voice` or `https://your-domain.com/voice` if using a reverse proxy with HTTPS).
   - If testing on a local server without a public IP, use a tool like `ngrok` to expose the port:
     ```bash
     ngrok http 5000
     ```
     Copy the provided public URL (e.g., `https://random-id.ngrok.io`) and append `/voice` to form the webhook URL.

2. **Set the Webhook in Twilio**:
   - Log in to your Twilio Console.
   - Navigate to "Phone Numbers" > "Manage" > Select your Twilio number.
   - Under "Voice & Fax", set the webhook URL for incoming calls to your endpoint (e.g., `https://your-domain.com/voice` or the ngrok URL).
   - Ensure the HTTP method is set to `POST`.

## Step 5: Test Inbound Calls with Twilio Webhooks

1. **Make Test Calls**:
   - Testing the application requires Twilio webhooks to be properly configured. Use a real phone number to call your Twilio number.
   - Verify that the call is routed to the correct person based on the day of the week as defined in `daily_assigner.py`.
   - Note that meaningful testing of the call routing functionality cannot be performed without Twilio webhooks set up.

2. **Monitor Logs**:
   - Check the container logs on the server for debugging:
     ```bash
     docker logs twilio-router
     ```
   - Look for entries like:
     - `Processing incoming call, fetching assigned person for today.`
     - `Incoming call on [Day], forwarding to [Name] at [Number]`
     - Any error messages if something fails.

3. **Debug Issues**:
   - If calls are not routing correctly, review the logs for errors related to Twilio API, environment variables, or assignment logic.
   - Restart the container if needed:
     ```bash
     docker restart twilio-router
     ```

## Step 6: Finalize Deployment

- Once testing confirms that inbound calls are routed correctly, ensure all environment variables are securely set and not hardcoded in the code.
- Set the container to restart automatically in case of server reboots:
  ```bash
  docker update --restart always twilio-router
  ```
- Document any specific server configurations or troubleshooting steps for future reference.
- Monitor the app periodically via Docker logs to ensure ongoing functionality.

## Troubleshooting

- **Webhook Not Triggering**: Verify the webhook URL in Twilio is correct and accessible. Test the endpoint with a tool like Postman or curl (e.g., `curl http://your-server-ip:5000/voice`). Ensure the server port is open and there are no firewall issues.
- **Environment Variables Missing**: Double-check that all required variables are set either in the `.env` file or as arguments in the `docker run` command.
- **Routing Errors**: Check logs for issues with `daily_assigner.py` logic or phone number retrieval.
- **Twilio Errors**: Ensure your Twilio account has sufficient credits and the phone number is active for inbound calls.
- **Container Not Running**: Use `docker ps -a` to check the status. If stopped, inspect logs with `docker logs twilio-router` for errors and restart if necessary.

For further assistance, refer to Docker documentation (https://docs.docker.com) or Twilio support (https://support.twilio.com).
