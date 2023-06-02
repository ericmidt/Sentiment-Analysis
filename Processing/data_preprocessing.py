import json
import os
import pandas as pd
import re
import pol_sub
import time
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/app/data', methods=["POST"])
def process_data():
    flask_data = request.json
    file_path = flask_data.get("filepath")
    with open(file_path, 'r') as json_file:
        raw_data = json.load(json_file)

    #while not os.path.exists(file_path):
        #time.sleep(120)
    raw_data_posts = [raw_data[subreddit] for subreddit in raw_data]

    # Removes subreddits and create list of posts

    list_of_dicts = [subreddit[_] for subreddit in raw_data_posts for _ in range(0, len(subreddit))]

    # Removes all distinction between submission and comment, creates a list of all available strings
    list_of_posts = [dict['title_and_post'] for dict in list_of_dicts
            ] + [comment for dict in list_of_dicts for comment in dict['comments'] if isinstance(comment, str)]
            
            # Removes all non-alphabetical characters except spaces
    def clean_text(text):
        text = re.sub(r"@[A-Za-z0–9]+", "", text) #Remove @mentions replace with blank
        text = re.sub(r"RT[\s]+", '', text) #Removing RT, replace with blank
        text = re.sub(r"https?:\/\/\S+", "", text) #Remove the hyperlinks
        text = re.sub(r"[^a-zA-Z áóíãé']", "", text) # Remove anything that's not alpha
        text = text.lower()
        return text

    clean_text_list = [clean_text(string) for string in list_of_posts]

    sub = [pol_sub.getPolarity(string) for string in clean_text_list]
    pol = [pol_sub.getSubjectivity(string) for string in clean_text_list]
    insight = [pol_sub.getInsight(polarity) for polarity in pol]

    # Create dataframe to better access data
    dataframe = pd.DataFrame({
        'Posts': clean_text_list,
        'Polarity': pol,
        'Subjectivity': sub,
        'Insight': insight
    })

    # Add sentiment column. 0: neutral, 1: positive, -1: negative
    #dataframe['sentiment'] = 0
    dataframe.to_csv('/app/Shared/posts_dataframe.csv')

    return "Data processed successfully."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    # Separate string into a list of words
    # words = raw_data_string.split()

    # Get rid of stopwords
    # stopwords_nltk = set(stopwords.words('english'))
    # cleaned_words = [word for word in lower_only if word not in stopwords_nltk]
