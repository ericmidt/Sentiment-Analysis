import reddit_credentials
import praw
import json

app_name = reddit_credentials.app_name
app_id = reddit_credentials.app_id
app_secret = reddit_credentials.app_secret
app_platform = reddit_credentials.app_platform
reddit_username = reddit_credentials.reddit_username
USER_AGENT = reddit_credentials.USER_AGENT

# Create the Reddit instance
reddit = praw.Reddit(client_id=app_id,
                     client_secret=app_secret,
                     user_agent=USER_AGENT)

# Define the keyword to search for
keyword = "python"

subreddits = [
    "careerguidance"
]
""" 
Subreddits to use when we fix performance issue:
"programming",
"learnprogramming",
"cscareerquestions",
"careerguidance",
"dailyprogrammer",
"coding",
"computerscience",
"SoftwareEngineering", 
"""

nr_posts = 10
nr_comments = 2
posts_data = {}
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(keyword, sort="comments", limit=nr_posts)
    posts_data[subreddit_name] = []
    
    for post in posts:
        post_data = {
            "title": post.title,
            "score": post.score,
            "comments": []
        }
        
        for comment in post.comments[:nr_comments]:
            post_data["comments"].append({
                "body": comment.body,
                "score": comment.score
            })
        
        posts_data[subreddit_name].append(post_data)
print(posts_data)

# Printing the posts_data dictionary
with open('reddit_data.json', 'w') as json_file:
    json.dump(posts_data, json_file, indent=4)

