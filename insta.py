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
