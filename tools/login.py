from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import json

SESSION_FILE = "static/json/session.json"
CREDENTIALS_FILE = "static/credentials.txt"

cl = Client()

def load_session():
    """Load Instagram session from file."""
   
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            file_content = f.read().strip()
            if file_content:
                session = json.loads(file_content)
                return session
            else:
                print("Session file is empty.")
                return None
    return None

def is_session_valid(session):
    """Check if the current session is valid"""
    try:
        cl.load_settings(session)
        cl.login()  
        return True
    except LoginRequired:
        print("Session is expired! Please login via username and password.")
        return False
    except Exception as e:
        print(f"Error during login via session: {e}")
        return False

def login_via_username_password(username, password):
    """Login to Instagram using username and password."""
    try:
        print(f"Attempting to login via username and password. Username: {username}")
        if cl.login(username, password):
            # Save session to a file
            session_data = cl.get_settings()
            with open(SESSION_FILE, "w") as f:
                json.dump(session_data, f, indent=4)
            return True
    except Exception as e:
        print(f"Couldn't login user using username and password: {e}")
    return False

def login_user():
    """Login to Instagram."""
    session = load_session()

    if session and is_session_valid(session):
        print("Successfully logged in via session.")

    # Get creds from file 
    with open(CREDENTIALS_FILE, "r") as f:
        USERNAME, PASSWORD = f.read().splitlines()

    if login_via_username_password(USERNAME, PASSWORD):
        print("Successfully logged in via username and password.")

    else:
        raise Exception("Can't login user with provided credentials")

