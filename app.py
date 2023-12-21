from instagrapi import Client
from instagrapi.exceptions import LoginRequired, FeedbackRequired
import os
import random
import time
import json
from datetime import datetime, timedelta
from tools.comments import COMMENTS
from tools.hashtags import HASHTAGS

CONFIG_FILE = "static/json/config.json"
SESSION_FILE = "static/json/session.json"
CREDENTIALS_FILE = "static/credentials.txt"
FOLLOWED_USERS_FILE = "static/followed_users.txt"

# Load configuration
with open(CONFIG_FILE, "r") as f:
    CONFIG = json.load(f)

def load_followed_users():
    """Load followed users from file."""
    followed_users = set()
    if os.path.exists(FOLLOWED_USERS_FILE):
        with open(FOLLOWED_USERS_FILE, "r") as f:
            lines = f.readlines()
            followed_users = set(line.strip() for line in lines if line.strip())
    return followed_users

def save_followed_user(username):
    """Save a followed user to the file."""
    followed_users = load_followed_users()
    followed_users.add(username)
    with open(FOLLOWED_USERS_FILE, "a") as f:
        f.write(username + "\n")

"""
    Basic functions for the bot, like, follow, comment, unfollow and more
"""
def like_post(cl, post, hashtag = None):
    if hashtag:
        try:
            cl.media_like(post.id)
            print(f"Liked post of {post.user.username} in hashtag {hashtag}")
        except FeedbackRequired as e:
            print(f"Feedback required: {e}")
            print(f"Skipping post due to feedback required: {post.id}")
            pass
        except Exception as e:
            print(f"Error interacting with post {post.id}: {e}")
    
    else:
        try:
            cl.media_like(post.id)
            print(f"Liked post of {post.user.username} from your {post}")
        except FeedbackRequired as e:
            print(f"Feedback required: {e}")
            print(f"Skipping post due to feedback required: {post.id}")
            pass
        except Exception as e:
            print(f"Error interacting with post {post.id}: {e}")


def follow_user(cl, user):
    try:
        followed_users = load_followed_users()
        if user.username not in followed_users:
            cl.user_follow(user.pk)
            print(f"Followed user {user.username}")
            save_followed_user(user.username)
        else:
            print(f"Already followed user {user.username}")
    except FeedbackRequired as e:
        print(f"Feedback required: {e}")
        print(f"Skipping follow due to feedback required: {user.pk}")
        pass
    except Exception as e:
        print(f"Error following user {user.username}: {e}")

def unfollow_user(cl, user):
    try:
        followed_users = load_followed_users()
        if user.username in followed_users:
            cl.user_unfollow(user.pk)
            print(f"unfollowed user {user.username}")
        else:
            print(f"You don't follow this user {user.username}")
    except FeedbackRequired as e:
        print(f"Feedback required: {e}")
        print(f"Skipping unfollow due to feedback required: {user.pk}")
        pass
    except Exception as e:
        print(f"Error unfollowing user {user.username}: {e}")

def comment_post(cl, post, comment):
    try:
        cl.media_comment(post.id, comment)
        print(f"Commented '{comment}' under post of {post.user.username}")
    except FeedbackRequired as e:
        print(f"Feedback required: {e}")
        print(f"Skipping comment due to feedback required: {post.id}")
        pass
    except Exception as e:
        print(f"Error commenting on post {post.id}: {e}")

def browse_home_feed(cl):
    print("fetching home feeds...")

    feed = cl.get_timeline_feed()
    try:
        home_feed = feed["data"]["user"]["edge_web_feed_timeline"]["edges"]
        print("Home feed structure:", home_feed)
        return home_feed
    except KeyError as e:
        print(f"Error accessing home feed: {e}")
        print("Complete feed data:", feed)
        return []


def browser_hashtags(cl, hashtag):
    print("Browsering hashtags....")
    
    medias = cl.hashtag_medias_recent(hashtag, 20)
    print(f"fetching post from {hashtag}")
    return medias

"""
    Login sessions, login via username and password or session
"""
def load_session():
    """Load Instagram session from file."""
    cl = Client()
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            file_content = f.read().strip()
            if file_content:
                session = json.loads(file_content)
                return cl, session
            else:
                print("Session file is empty.")
                return cl, None
    return cl, None

def is_session_valid(cl, session):
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

def login_via_username_password(cl, username, password):
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
    cl, session = load_session()

    if session and is_session_valid(cl, session):
        print("Successfully logged in via session.")
        return cl

    # Get creds from file 
    with open(CREDENTIALS_FILE, "r") as f:
        USERNAME, PASSWORD = f.read().splitlines()

    if login_via_username_password(cl, USERNAME, PASSWORD):
        print("Successfully logged in via username and password.")
        return cl
    else:
        raise Exception("Can't login user with provided credentials")

# Main program
def main():
    # Config
    SLEEP_INTERVALS = CONFIG.get("SLEEP_INTERVALS")
    BOT_CHOICE = CONFIG.get("BOT_CHOICE")
    max_likes = CONFIG.get("MAX_LIKES_PER_SESSION")
    max_follows = CONFIG.get("MAX_FOLLOWS_PER_SESSION")
    max_comments = CONFIG.get("MAX_COMMENTS_PER_SESSION")

    def get_sleep_interval():
        seconds = random.choice(SLEEP_INTERVALS)
        print(f"Sleeping for {seconds} seconds...")
        return time.sleep(seconds)
    
    def get_bot_choice():
        if BOT_CHOICE:
           choice = random.choice(BOT_CHOICE)
           print("Bot says:", choice)
           return choice
        else:
            return "N"

    
    # Log in
    cl = login_user()

    try:

        while True:
            # Perform random actions
            print("Starting bot...")
            choice = get_bot_choice()

            if choice == "Yes":
                # Browse and interact with hashtags
                hashtag = random.choice(HASHTAGS)
                medias = browser_hashtags(cl, hashtag)
                # home_feed = browse_home_feed(cl)

                # Simulate human-like behavior
                # get_sleep_interval()

                likes_count, follows_count, comments_count = 0, 0, 0

                for i, media in enumerate(medias):
                    comment = random.choice(COMMENTS)

                    if choice == "Yes" and likes_count < max_likes:
                        like_post(cl, media, hashtag)
                        likes_count += 1

                    choice = get_bot_choice()
                    if choice == "Yes" and comments_count < max_comments:
                        comment_post(cl, media, comment)
                        comments_count += 1
                        get_sleep_interval()

                    choice = get_bot_choice()
                    if choice == "Yes" and follows_count < max_follows:
                        follow_user(cl, media.user)
                        follows_count += 1
                        get_sleep_interval()

                    # Check if the interaction limits are reached
                    if likes_count >= max_likes and comments_count >= max_comments and follows_count >= max_follows:
                        break

            else:
                # If the bot is not active, wait for a longer sleep interval
                print("Bot is inactive. Waiting for a longer interval...")
                time.sleep(3)
            
            continue
    except KeyboardInterrupt:
        print("Bot interrupted by user.")

if __name__ == "__main__":
    main()



