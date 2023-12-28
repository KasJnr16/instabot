import os

"""
    Keeps track of users the bot follows
"""

FOLLOWED_USERS_FILE = "static/followed_users.txt"

def create_followed_file():
    """Creates followed_users file if it doesn't exist."""
    try:
        with open(FOLLOWED_USERS_FILE, 'w') as f:
            pass 
    except Exception as e:
        print("file error:",e)
        
def load_followed_users():
    """Load followed users from file."""
    followed_users = set()
    if os.path.exists(FOLLOWED_USERS_FILE):
        with open(FOLLOWED_USERS_FILE, "r") as f:
            lines = f.readlines()
            followed_users = set(line.strip() for line in lines if line.strip())
    else:
        create_followed_file()
        load_followed_users()
    return followed_users

def save_followed_user(username):
    """Save a followed user to the file."""
    followed_users = load_followed_users()
    followed_users.add(username)
    with open(FOLLOWED_USERS_FILE, "a") as f:
        f.write(username + "\n")