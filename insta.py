from instagrapi import Client
from dotenv import load_dotenv
import os
import random as r
import time
import json
from datetime import datetime, timedelta
import schedule

follower_threshold = 800  
follow_businesses = False
maximum_follows_per_session = 5  
min_unfollow_days = 3 
max_unfollow_days = 7 
follow_log_file = "follow_log.json" 

client = Client()
load_dotenv()
USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def load_follow_log():
    if os.path.exists(follow_log_file):
        try:
            with open(follow_log_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_follow_log(log):
    with open(follow_log_file, "w") as f:
        json.dump(log, f, indent=2)    

def record_follow(user_pk, username):
    log = load_follow_log()
    wait_days = r.uniform(min_unfollow_days, max_unfollow_days)
    unfollow_after = datetime.now() + timedelta(days=wait_days)
    log[str(user_pk)] = {
        "username": username,
        "followed_at": datetime.now().isoformat(),
        "unfollow_after": unfollow_after.isoformat(),
    }
    save_follow_log(log)

def login_user():
    session_file = "session.json"

    if os.path.exists(session_file):
        client.load_settings(session_file)

        try:
            client.login(USERNAME, PASSWORD)
            client.get_timeline_feed()
            return

        except Exception as e:
            old_settings = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_settings["uuids"])

    client.login(USERNAME, PASSWORD)
    client.dump_settings(session_file)


already_following = set()  # Populated at startup

def load_following():
    global already_following
    try:
        following = client.user_following(client.user_id)  # dict keyed by user_pk
        already_following = set(str(pk) for pk in following.keys())
        print(f"Loaded {len(already_following)} existing followings")
    except Exception as e:
        print(f"Could not load following list: {e}")
        already_following = set()

def check_user(user_id: str):
    try:
        info = client.user_info(user_id)
    except Exception:
        return False  # Skip user

    # Skip business/creator accounts unless explicitly allowed
    if not follow_businesses and info.is_business:
        return False

    # Only follow accounts under the follower threshold
    if info.follower_count >= follower_threshold:
        return False

    # Don't follow people we already follow
    if str(user_id) in already_following:
        return False

    return True
