from instagrapi.exceptions import FeedbackRequired, HashtagError, LoginRequired, ClientError
from .manage_users import load_followed_users, save_followed_user
from .import hashtags, comments
import random

def random_hashtags():
    return random.choice(hashtags.HASHTAGS)

def random_comment():
    return random.choice(comments.COMMENTS)

def retry_hashtags(cl):
    print(f"Trying another hashtag....")
    try:
        hashtag = random_hashtags()
        hashtag_medias = cl.hashtag_medias_recent(hashtag, 20)
        print(f"fetching post from {hashtag}")
        return hashtag_medias
    except (LoginRequired,
            ClientError,

            ) as e:
        print(f"Feedback required: {e}")
        print(f"Skipping {hashtag} due to error")
        retry_hashtags(cl)

    except Exception as e:
        print(f"Hashtag error: {e}")

    finally:
        print("Failed to use hashtag")

"""
    Every actions the bot takes are present here, feel free to modify if you want :)~
"""

# Global Variable
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
            print(f"Liked post of {post.user.username} number {post.id}")
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

def browse_hashtags(cl, hashtag):
    print("Browsering hashtags....")
    try: 
        hashtag_medias = cl.hashtag_medias_recent(hashtag, 20)
        print(f"fetching post from {hashtag}")
        return hashtag_medias

    except Exception as e:
        try:
            hashtag_medias = cl.hashtag_medias_recent_a1(hashtag, 20)
        except ClientError:
            hashtag_medias = cl.hashtag_medias_recent_v1(hashtag, 20)
        return hashtag_medias
    
def browse_reels(cl):
    print("fetching Reels...")
    reels = cl.reels(10)
    return reels

def browse_user_profile(cl, user):
    print(f"fetching data from {user}'s profile...")
    try:                                               
        user_profile_media = cl.user_medias(user_id=user)
        return user_profile_media
    except LoginRequired as e:
        print("Error:", e)
        print("Skipping reel")

