from instagrapi import Client
from instagrapi.exceptions import FeedbackRequired
from datetime import datetime, timedelta
from .manage_users import load_followed_users, save_followed_user
from .import hashtags, comments
import random

def random_hashtags():
    return random.choice(hashtags.HASHTAGS)

def random_comment():
    return random.choice(comments.COMMENTS)


"""
    Every actions the bot takes are present here, feel free to modify if you want :)~
"""

# Global Variable
cl = Client()

def like_post(post, hashtag = None):
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
            print(f"Liked post of {post.user.username} number {post.id}")
        except FeedbackRequired as e:
            print(f"Feedback required: {e}")
            print(f"Skipping post due to feedback required: {post.id}")
            pass
        except Exception as e:
            print(f"Error interacting with post {post.id}: {e}")

def follow_user(user):
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

def unfollow_user(user):
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

def comment_post(post, comment):
    try:
        cl.media_comment(post.id, comment)
        print(f"Commented '{comment}' under post of {post.user.username}")
    except FeedbackRequired as e:
        print(f"Feedback required: {e}")
        print(f"Skipping comment due to feedback required: {post.id}")
        pass
    except Exception as e:
        print(f"Error commenting on post {post.id}: {e}")

def browse_hashtags(hashtag):
    print("Browsering hashtags....")
    
    hashtag_medias = cl.hashtag_medias_recent(hashtag, 20)
    print(f"fetching post from {hashtag}")
    return hashtag_medias

def browse_user_profile(user):
    print(f"fetching data from {user.username}'s profile...")

    user_profile_media = cl.user_medias_gql(user_id=user.id)
    return user_profile_media