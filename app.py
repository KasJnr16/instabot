from instagrapi import Client

from tools.login import login_user
from tools.bot_actions import (
    like_post,
    comment_post,
    follow_user,
    unfollow_user,
    browse_hashtags,
    browse_user_profile,
    browse_reels,
    # more actions will be addded later

    random_comment,
    random_hashtags,
)
from tools.manage_users import load_followed_users

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
            return "No"
        
    # login
    cl = login_user()
    try:
        print("""
                            _         _______  _______  _______  _______    _______  _______  _______ 
                            ( \      (  ___  )(  ____ \(  ____ \(  ____ \  (  ____ \(  ____ \(  ____ \ 
                            | (      | (   ) || (    \/| (    \/| (    \/  | (    \/| (    \/| (    \/
                            | |      | |   | || (__    | (__    | (__      | (__    | (__    | (__    
                            | |      | |   | ||  __)   |  __)   |  __)     |  __)   |  __)   |  __)   
                            | |      | |   | || (      | (      | (        | (      | (      | (      
                            | (____/\| (___) || (____/\| (____/\| (____/\  | (____/\| (____/\| (____/\ 
                            (_______/(_______)(_______/(_______/(_______/  (_______/(_______/(_______/
                                Welcome to Insta Bot! 🤖✨
            """)
        time.sleep(3)
        while True:
            for i in range(5):
                print("Starting bot in %i" % i)
                time.sleep(1)

            choice = get_bot_choice()
            if choice == "Yes":

                #limit activity to avoid being to spammy
                likes_count, follows_count, comments_count = 0, 0, 0

                hashtag = random_hashtags()
                comment = random_comment()

                # followed_user = load_followed_users()
                # user_profile = browse_user_profile()
                
                # hashtag_medias = browse_hashtags(cl, hashtag)
                reels = browse_reels(cl)
                
                for i, post in enumerate(reels):

                    """ 
                    Decides which activity to perform on every iterationm :)~ using the bot choice
                    
                    """
                    choice = get_bot_choice()
                    if choice == "Yes" and likes_count < max_likes:
                        like_post(cl, post)
                        sleep_interval = get_sleep_interval()
                        likes_count += 1

                    choice = get_bot_choice()
                    if choice == "Yes" and comments_count < max_comments:
                        comment_post(cl, post, comment)
                        sleep_interval = get_sleep_interval()
                        comments_count +=1
                    
                    choice = get_bot_choice()
                    if choice == "Yes" and follows_count >= max_follows:
                        follow_user(cl, post)
                        follows_count+=1

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



