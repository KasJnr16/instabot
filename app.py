from instagrapi import Client

from tools.login import login_user
from tools.bot_actions import (
    like_post,
    comment_post,
    follow_user,
    unfollow_user,
    browse_hashtags,
    browse_user_profile,
    # more actions will be addded later

    random_comment,
    random_hashtags,
)

import random
import time
import json
from datetime import datetime, timedelta

CONFIG_FILE = "static/json/config.json"

# Load configuration
if CONFIG_FILE:
    with open(CONFIG_FILE, "r") as f:
        CONFIG = json.load(f)

else:
    with open(CONFIG_FILE, "w") as f:
        pass

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
        
    # login
    login = login_user()
    try:

        while True:
            for i in range(5):
                print("Starting bot in %i" % i)
                time.sleep(1)

            choice = get_bot_choice()

            if choice == "Yes":

                likes_count, follows_count, comments_count = 0, 0, 0

               

                    # Check if the interaction limits are reached
                if likes_count >= max_likes and comments_count >= max_comments and follows_count >= max_follows:
                    break

            else:
                # If the bot is not active, wait for a longer sleep interval
                print("Bot is inactive. Waiting for a 3 secs...")
                time.sleep(5)
            
            continue
    except KeyboardInterrupt:
        print("Bot interrupted by user.")

if __name__ == "__main__":
    main()



