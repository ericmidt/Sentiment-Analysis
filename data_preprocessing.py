import json
from nltk.corpus import stopwords

# import reddit_streamer
# raw_data = reddit_streamer.reddit_raw_data

with open('reddit_data.json') as json_file:
    raw_data = json.load(json_file)

# Convert the JSON data to a string
raw_data_string = json.dumps(raw_data)

# Separate string into a list of words
words = raw_data_string.split()

# Remove non alphabetic characters
alphabetic_only = [word for word in words if word.isalpha()]

# Convert all words to lower case
lower_only = [word.lower() for word in alphabetic_only]

# Get rid of stopwords
stopwords_nltk = set(stopwords.words('english'))
cleaned_words = [word for word in lower_only if word not in stopwords_nltk]
 