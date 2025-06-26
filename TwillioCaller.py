# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
from daily_assigner import PHONE_DIRECTORY

# Load environment variables for credentials
load_dotenv()

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")

# Check if credentials are loaded
if not account_sid or not auth_token or not from_number:
    print("Error: Twilio credentials or from number not found in environment variables.")
    print("Please ensure TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER are set in your .env file.")
    exit(1)

client = Client(account_sid, auth_token)

def initiate_call(to_number, person_name):
    """
    Initiates a call to the specified number using Twilio API.
    Returns the call SID if successful, or an error message if failed.
    """
    try:
        print(f"Initiating call to {person_name} at {to_number}...")
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",  # Using demo TwiML for simplicity; adjust if custom TwiML is needed
            to=to_number,
            from_=from_number,
            status_callback="http://your-server-url/call-status",  # Replace with actual server URL in production
            status_callback_method="POST",
            status_callback_event=["initiated", "ringing", "answered", "completed"]
        )
        print(f"Call initiated successfully to {person_name}. Call SID: {call.sid}")
        return call.sid
    except TwilioRestException as e:
        print(f"Failed to initiate call to {person_name}. Error: {str(e)}")
        return None

def test_call_all_individuals():
    """
    Loops through all individuals in PHONE_DIRECTORY and initiates a call to each.
    Logs the result of each call attempt.
    """
    print("Starting test to call all individuals in PHONE_DIRECTORY...\n")
    
    for person_name, phone_number in PHONE_DIRECTORY.items():
        if phone_number:
            initiate_call(phone_number, person_name)
        else:
            print(f"No phone number found for {person_name}. Skipping...")
        print("-" * 50)
    
    print("\nTest completed. All individuals have been attempted.")

if __name__ == "__main__":
    test_call_all_individuals()
