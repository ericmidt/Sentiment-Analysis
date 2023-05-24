import praw
import json
import reddit_credentials
import boto3


app_name = reddit_credentials.app_name
app_id = reddit_credentials.app_id
app_secret = reddit_credentials.app_secret
app_platform = reddit_credentials.app_platform
reddit_username = reddit_credentials.reddit_username
reddit_pw = reddit_credentials.reddit_password
USER_AGENT = reddit_credentials.USER_AGENT
s3_bucket_name = reddit_credentials.s3_bucket

# Create the Reddit instance
reddit = praw.Reddit(client_id=app_id,
                     client_secret=app_secret,
                     user_agent=USER_AGENT,
                     username=reddit_username,
                     password=reddit_pw)

# Allows test with only one subreddit
""" subreddit_names = ["careerguidance"] """

# Subreddits that will be used in the search
subreddit_names = ["careerguidance", 
                    "programming",
                    "learnprogramming",
                    "cscareerquestions",
                    "careerguidance",
                    "dailyprogrammer",
                    "coding",
                    "computerscience",
                    "SoftwareEngineering"
                    ]

#Define post, comment and comment tree limits
post_limit = 300  # Number of posts to retrieve
comment_limit = 10  # Number of comments per post
comment_tree_limit = 5  # Number of comment trees per post

data_dict = {}
keyword = "python"
# Fetch subreddit data for multiple subreddits
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(keyword, sort="new", limit=post_limit)
    data_list = []
    # Filter for certain keywords in the title and read the first comment tree
    for post in posts:
        if keyword in post.title:
            title = post.title
            post.comments.replace_more(limit=comment_tree_limit)
            comment_tree = post.comments.list()[:comment_tree_limit]  # Read limited comment trees
            comment_data = []
            for comment in comment_tree:
                # Only adds comment if it has the keyword
                if keyword in comment.body:
                    comment_data.append(comment.body)
                    if len(comment.replies) > 0:
                            reply_data = []
                            for reply in comment.replies[:comment_limit]:
                                # Only adds reply if it has the keyword
                                if keyword in reply_data:
                                    reply_data.append(reply.body)
                            comment_data.append(reply_data)
            data_list.append({
                'subreddit': subreddit_name,
                'title': title,
                'comments': comment_data,
            })
        data_dict[subreddit_name] = data_list

filename = 'reddit_data.json'
with open(filename, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)  # Pretty print with indent=4
print(f"Data saved as {filename}") 

# Create an S3 client
s3_client = boto3.client('s3')

# Upload the JSON file to S3
with open(filename, 'rb') as file:
    s3_client.put_object(Body=filename, Bucket=s3_bucket_name, Key='redditrawdata.json')
