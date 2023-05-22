import os
from dotenv import load_dotenv
import praw

# Setup up IDs and variables from .env local file.
load_dotenv("C:/Python/EnvironmentVariables/.env")
app_name = os.environ.get("reddit_app_name")
app_id = os.environ.get("reddit_app_id")
app_secret = os.environ.get("reddit_app_secret")
app_platform = os.environ.get("reddit_app_platform")
reddit_username = os.environ.get("reddit_username")

USER_AGENT = "windows:" + f"localhost:{app_name}:v1 (by /u/" + reddit_username + ")"

# Create the Reddit instance
reddit = praw.Reddit(client_id=app_id,
                     client_secret=app_secret,
                     user_agent=USER_AGENT)

# Specify the subreddit to search
subreddit = reddit.subreddit("python")

# Retrieve the top posts from the subreddit
posts = subreddit.top(limit=10)

# Iterate over the posts and print their titles
for post in posts:
    print(post.title)
