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


client = Client()
load_dotenv()
USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


