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

def follow_users(num_users: int, hashtag: str):
    load_following()
    followings_left = num_users

    while followings_left > 0:
        medias = client.hashtag_medias_recent(hashtag, num_users * 3)

        for media in medias:
            if followings_left <= 0:
                break

            potential_user = media.user

            # Look at each candidate, then pause as if reading their profile
            if not check_user(potential_user.pk):
                time.sleep(r.uniform(2, 6))
                continue

            try:
                client.user_follow(potential_user.pk)
                record_follow(potential_user.pk, potential_user.username)
                followings_left -= 1
                print(f"Followed {potential_user.username} ({num_users - followings_left}/{num_users})")
            except Exception as e:
                print(f"Failed to follow {potential_user.username}: {e}")

            # Long gap between follows
            time.sleep(r.uniform(30, 90))

        # Wait before pulling next batch of posts
        if followings_left > 0:
            time.sleep(r.uniform(120, 300))


def unfollow_due_users():
    log = load_follow_log()
    now = datetime.now()
    due = [pk for pk, rec in log.items()
           if now >= datetime.fromisoformat(rec["unfollow_after"])]

    if not due:
        return

    for pk in due:
        username = log[pk]["username"]
        try:
            client.user_unfollow(pk)
            print(f"Unfollowed {username}")
            del log[pk]  # Remove only on success so failures are retried next pass
            save_follow_log(log)
        except Exception as e:
            print(f"Failed to unfollow {username}: {e}")

        # Delay
        time.sleep(r.uniform(30, 90))


def schedule_todays_sessions():
    schedule.clear("sessions")  # Drop yesterday's slots before creating today's

    num_sessions = r.randint(1, 2)
    chosen_times = []

    while len(chosen_times) < num_sessions:
        # Random time of day, kept within waking hours to look natural
        hour = r.randint(8, 22)
        minute = r.randint(0, 59)
        slot = f"{hour:02d}:{minute:02d}"
        # Avoid two sessions landing in the same hour
        if all(abs(hour - int(t[:2])) >= 2 for t in chosen_times):
            chosen_times.append(slot)

    for slot in chosen_times:
        schedule.every().day.at(slot).do(run_session).tag("sessions")

    print(f"Scheduled {num_sessions} session(s) today at: {', '.join(sorted(chosen_times))}")
    
login_user()

# Re-roll the day's session times every midnight so they aren't fixed
schedule.every().day.at("00:01").do(schedule_todays_sessions)

# Lay down today's schedule immediately on startup rather than waiting for midnight
schedule_todays_sessions()

while True:
    schedule.run_pending()
    time.sleep(30)

run_session()    
