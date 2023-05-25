import json
from nltk.corpus import stopwords
import os
import pandas as pd
import re
import pol_sub

# Clear screen to make testing the code easier
os.system('cls')

# import reddit_streamer
# raw_data = reddit_streamer.reddit_raw_data

with open('reddit_data.json') as json_file:
    raw_data = json.load(json_file)
    print('ok')

raw_data_posts = [raw_data[subreddit] for subreddit in raw_data]

# Removes subreddits and create list of posts
list_of_dicts = []
for subreddit in raw_data_posts:
    for _ in range(0, len(subreddit)):
        list_of_dicts.append((subreddit[_]))

# Removes all distinction between submission and comment, creates a list of all available strings
list_of_posts = []
for dict in list_of_dicts:
    list_of_posts.append(dict['title_and_post'])
    for comment in dict['comments']:
        # filters empty comments from new list
        if type(comment) == str:
            list_of_posts.append(comment)

# Removes all non-alphabetical characters except spaces
def clean_text(text):
    text = re.sub(r'@[A-Za-z0–9]+', '', text) #Remove @mentions replace with blank
    text = re.sub(r'RT[\s]+', '', text) #Removing RT, replace with blank
    text = re.sub(r'https?:\/\/\S+', '', text) #Remove the hyperlinks
    text = re.sub(r'[^a-zA-Z áóíãé]', '', text) # Remove anything that's not alpha
    text = text.lower()
    return text

clean_text_list = []
for string in list_of_posts:
    clean_text_list.append(clean_text(string))

sub = []
pol = []
for string in clean_text_list:
    pol.append(pol_sub.getPolarity(string))

for string in clean_text_list:
    sub.append(pol_sub.getSubjectivity(string))


dataframe = pd.DataFrame({
    'Posts': list_of_posts,
    'Sentiment': pol,
    'Subjectivity': sub
})
dataframe.index.name = 'Index'

# Create dataframe to better access data
'''dataframe = pd.DataFrame(clean_text_list, columns=['posts'])
dataframe = pd.DataFrame(pol, columns=['polarity'])
dataframe = pd.DataFrame(sub, columns=['subjectivity'])
'''
# Add sentiment column. 0: neutral, 1: positive, -1: negative
#dataframe['sentiment'] = 0
dataframe.to_csv('posts_dataframe.csv')

# Separate string into a list of words
# words = raw_data_string.split()

# Get rid of stopwords
# stopwords_nltk = set(stopwords.words('english'))
# cleaned_words = [word for word in lower_only if word not in stopwords_nltk]
