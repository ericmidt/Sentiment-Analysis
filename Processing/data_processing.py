import json
import pandas as pd
import re
import pol_sub
from flask import Flask, request

app = Flask(__name__)

@app.route('/app/data', methods=["POST"])
def process_data():
    flask_data = request.json
    file_path = flask_data.get("filepath")
    with open(file_path, 'r') as json_file:
        raw_data = json.load(json_file)

    # Removes all distinction between submission and comment, creates a list of all available strings
    list_of_posts = raw_data
            
            # Removes all non-alphabetical characters except spaces
    def clean_text(text):
        text = re.sub(r"@[A-Za-z0–9]+", "", text) #Remove @mentions replace with blank
        text = re.sub(r"RT[\s]+", '', text) #Removing RT, replace with blank
        text = re.sub(r"https?:\/\/\S+", "", text) #Remove the hyperlinks
        text = re.sub(r"[^a-zA-Z áóíãé']", "", text) # Remove anything that's not alpha
        text = text.lower()
        return text

    clean_text_list = [clean_text(string) for string in list_of_posts]

    pol = [pol_sub.getPolarity(string) for string in clean_text_list]
    sub = [pol_sub.getSubjectivity(string) for string in clean_text_list]
    insight = [pol_sub.getInsight(polarity) for polarity in pol]

    # Create dataframe to better access data
    dataframe = pd.DataFrame({
        'Comments': clean_text_list,
        'Polarity': pol,
        'Subjectivity': sub,
        'Insight': insight
    })

    # Add sentiment column. 0: neutral, 1: positive, -1: negative
    dataframe.to_csv('/app/Shared/posts_dataframe.csv')

    return "Data processed successfully."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)