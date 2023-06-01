import praw
import json
#import reddit_credentials
import boto3


app_name = "sent_analysis_br"
app_id = "qURatL5KzO7NYjJrehM_uw"
app_secret = "WQHmtHM_NT0U3DfpHW3IS5XltWTelA"
app_platform = "script"
reddit_username = "FlingoLingo_Potato"
reddit_pw = "Garagem9@"
USER_AGENT = "windows:" + f"localhost:{app_name}:v1 (by /u/" + reddit_username + ")"
s3_bucket_name = "emilio-bucketo"

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
    posts = subreddit.search(keyword, sort="best", limit=post_limit)
    data_list = []
    # Filter for certain keywords in the title and read the first comment tree
    for post in posts:
        if keyword in post.title:
            title = post.title
            post_text = post.selftext
            post.comments.replace_more(limit=comment_tree_limit)
            comment_tree = post.comments.list()[:comment_tree_limit]  # Read limited comment trees
            comment_data = []
            for comment in comment_tree:
                # Only adds comment if it has the keyword
                if keyword in comment.body:
                    comment_data.append(comment.body)
                    if len(comment.replies) > 0:
                            reply_data = []
                            reply_data = [reply.body for reply in comment.replies[:comment_limit] if keyword in reply_data]
                            comment_data.append(reply_data)
            data_list.append({
                'title_and_post': title + " " + post_text,
                'comments': comment_data,
            })
        data_dict[subreddit_name] = data_list

filename = '/app/Shared/reddit_data.json'
with open(filename, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)  # Pretty print with indent=4
print(f"Data saved at {filename}") 

# Create an S3 client
#s3_client = boto3.client('s3')

# Specify the file key
file_key = 'redditrawdata.json'

# Upload the JSON file to S3
#with open(filename, 'rb') as file:
#    s3_client.put_object(Body=file, Bucket=s3_bucket_name, Key=file_key)

# Downloads file
""" s3_client.download_file('rawredditdata', 'redditrawdata.json', 'redditrawdata.json') """

# Retrieve the file object
#response = s3_client.get_object(Bucket=s3_bucket_name, Key=file_key)

# Read the content of the file
#reddit_raw_data = response['Body'].read().decode('utf-8')
