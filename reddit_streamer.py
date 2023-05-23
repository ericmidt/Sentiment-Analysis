import praw
import json

import reddit_credentials


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


# Define the list of subreddit names
subreddit_names = ['CryptoMarkets', 'CryptoCurrency', 'Altcoin']


#Define post, comment and comment tree limits
post_limit = 100  # Number of posts to retrieve
comment_limit = 10  # Number of comments per post
comment_tree_limit = 5  # Number of comment trees per post

data_dict = {}

# Fetch subreddit data for multiple subreddits
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=post_limit)

    data_list = []

    # Filter for certain keywords in the title and read the first comment tree
    for post in posts:
        title = post.title
        if 'bitcoin' in title or 'crypto' in title or 'trading' in title or 'bot' in title or 'tether' in title or 'bnb' in title or 'dogecoin' in title:
            post.comments.replace_more(limit=comment_tree_limit)
            comment_tree = post.comments.list()[:comment_tree_limit]  # Read limited comment trees


            comment_data = []
            for comment in comment_tree:
                comment_data.append(comment.body)

                if len(comment.replies) > 0:
                        reply_data = []
                        for reply in comment.replies[:comment_limit]:
                            reply_data.append(reply.body)
                        comment_data.append(reply_data)

            data_list.append({
                'subreddit': subreddit_name,
                'title': title,
                'comments': comment_data,
            })
        
    data_dict[subreddit_name] = data_list
            

for subreddit_name, data_list in data_dict.items():
    filename = f'{subreddit_name}_data.json'
    with open(filename, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)  # Pretty print with indent=4

    print(f"Data for {subreddit_name} saved as {filename}")