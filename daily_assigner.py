import datetime
from dotenv import load_dotenv
import os


#set names as constants for easy reference to avoid typos
# Define constants for names
EDWARD = "EDWARD"
JOHNNY_R = "JOHNNY_R"
CHRIS = "CHRIS"
JOHNNATHAN = "JOHNNATHAN"
DEFAULT_CONTACT = "DEFAULT_CONTACT"

# Define your phone number mapping
# Replace XXXXXXXXXX with actual phone numbers

# Load environment variables from .env file
load_dotenv()

PHONE_DIRECTORY = {
    "EDWARD": os.getenv(EDWARD),
    "JOHNNY_R": os.getenv(JOHNNY_R),
    "CHRIS": os.getenv(CHRIS),
    "JOHNNATHAN": os.getenv(JOHNNATHAN),
    "DEFAULT_CONTACT": os.getenv(DEFAULT_CONTACT)
}



# Define the schedule: 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
# Assign names directly here for simplicity in the console app
DAILY_ASSIGNMENTS = {
    0: JOHNNY_R,  # Monday
    1: EDWARD,    # Tuesday
    2: CHRIS,     # Wednesday
    3: CHRIS,     # Thursday (Changed from AnotherPerson to Chris)
    4: EDWARD,    # Friday
    5: CHRIS , # Saturday
    6: EDWARD  # Sunday
}

DEFAULT_ASSIGNEE_NAME = PHONE_DIRECTORY[DEFAULT_CONTACT]  # Default contact if no assignment is found

def get_assigned_person_for_today(test_todays_day=None):
    """
    Determines the assigned person and their phone number for the current day.
    Optionally, a specific day of the week can be passed for testing.
    """
    import logging
    try:    
        if test_todays_day is None:
            current_day_of_week = datetime.datetime.now().weekday()  # Monday is 0 and Sunday is 6
            logging.info("Fetching current day of week for assignment.")
        else:
            current_day_of_week = test_todays_day
            logging.info(f"Using test day index {current_day_of_week} for assignment.")
        
        assigned_name = DAILY_ASSIGNMENTS.get(current_day_of_week, DEFAULT_ASSIGNEE_NAME)
        phone_number = PHONE_DIRECTORY.get(assigned_name, PHONE_DIRECTORY[DEFAULT_ASSIGNEE_NAME])
        
        logging.info(f"Assigned person for day {current_day_of_week}: {assigned_name} with number {phone_number}")
        return assigned_name, phone_number, datetime.datetime.now().strftime("%A")
    except Exception as e:
        logging.error(f"Error getting assigned person: {str(e)}")
        return DEFAULT_ASSIGNEE_NAME, PHONE_DIRECTORY[DEFAULT_ASSIGNEE_NAME], datetime.datetime.now().strftime("%A")

if __name__ == "__main__":
    # Test with current day
    assigned_name, phone_number, day_name = get_assigned_person_for_today()
    print(f"Today is {day_name}.")
    print(f"The assigned person is: {assigned_name}")
    print(f"Their phone number is: {phone_number}")

    # Test with a specific day (e.g., Monday which is 0)
    print("--- Testing for entire week ---")
    test_day_number = 0
    for test_day_number in range(6):
        # Note: The day_name returned will still be today's name, as strftime("%A") uses current time.
        # If you need the day name for the test_day_number, you'd adjust that part of the return too.
        assigned_name, phone_number, _ = get_assigned_person_for_today(test_todays_day=test_day_number)
        #convert day number to day name for display
        day_name = datetime.datetime(2023, 1, 1 + test_day_number).strftime("%A")
        print(f"Day {day_name} ({test_day_number}):")
        print(f"The assigned person is: {assigned_name}")
        print(f"Their phone number is: {phone_number}")
        test_day_number += 1
    print("--- End of tests ---")
