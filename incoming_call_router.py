from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Dial
import logging
import datetime
# Import the function from your daily_assigner.py file
from daily_assigner import get_assigned_person_for_today

app = Flask(__name__)

# Configure logging with timestamps and detailed format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/voice", methods=['POST'])
def voice_webhook():
    """Responds to incoming calls with TwiML to forward the call."""
    try:
        response = VoiceResponse()
        dial = Dial()
        
        # Get the assigned person's name, phone number, and the day name
        logging.info("Processing incoming call, fetching assigned person for today.")
        assigned_name, target_number, day_name = get_assigned_person_for_today()
        
        if not target_number:
            error_msg = f"No valid phone number found for {assigned_name} on {day_name}. Using default if available."
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        logging.info(f"Incoming call on {day_name}, forwarding to {assigned_name} at {target_number}")
        dial.number(target_number)
        response.append(dial)
        
        logging.info("Successfully generated TwiML response for call routing.")
        return str(response)
    except Exception as e:
        logging.error(f"Error processing incoming call: {str(e)}")
        response = VoiceResponse()
        response.say("Sorry, we encountered an error. Please try again later.")
        return str(response)

@app.route("/call-status", methods=['POST'])
def call_status_webhook():
    """Handles call status updates from Twilio."""
    try:
        status = request.form.get('CallStatus')
        call_sid = request.form.get('CallSid')
        logging.info(f"Call status update received for Call SID: {call_sid}, Status: {status}")
        return {"status": "received"}, 200
    except Exception as e:
        logging.error(f"Error processing call status update: {str(e)}")
        return {"status": "error"}, 500

@app.route("/health", methods=['GET'])
def health_check():
    """Returns a simple health status for the service."""
    logging.info("Health check endpoint accessed.")
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # For development purposes only. Use a proper WSGI server for production.
    app.run(debug=True, port=5000)
