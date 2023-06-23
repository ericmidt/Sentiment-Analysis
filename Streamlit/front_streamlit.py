import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time
import os
import requests
from flask import Flask, request

def load_page():
    # Read the channel name from the .txt file

    file_path = '/app/Shared/channel_name.json'

    if os.path.exists(file_path):

        channel_name_file = file_path

        with open(channel_name_file, 'r') as json_file:

            channel_name = json_file.read().strip()

    else:

        print("File does not exist.")

    channel_name = " dhuiashdsa "
    # Cancel warning in streamlit
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_page_config(page_title="Youtube Sentiment Analysis")
    st.title(f"Youtube Channel: {channel_name}")
    # Create sidebar
    st.sidebar.header("YouTube Channel Sentinment Analysis")
    st.sidebar.subheader("Options")
    
    # Add input field for channel name
    new_channel_name = st.sidebar.text_input(label="Enter new YouTube channel name", label_visibility="hidden", placeholder="NewChannelName")

    # Add button to trigger channel name update
    if st.sidebar.button("Update Channel Name"):
        # Send channel name to the appropriate container
        url = "http://data_preprocessing:8080/app/data"
        flask_data = {"channel_name": new_channel_name}
        response = requests.post(url=url, json=flask_data)

        if response.status_code == 200:
            st.sidebar.success("Channel name updated successfully.")
        else:
            st.sidebar.error("Error updating channel name.")


    def generate_wordcloud(data, stopwords_list):
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, stopwords=stopwords_list).generate(data)
        st.title("Word Cloud")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()

    def generate_chart(data):
        st.title("Sentiment Chart")
        data.plot(kind='bar')
        plt.xlabel("Sentiment")
        plt.ylabel("Number of posts")
        plt.show()
        st.pyplot()

    def generate_dataframe(data):
        st.title("Comments Data Frame")
        st.dataframe(data)
        st.pyplot()

    stopwords = STOPWORDS
    additional_stopwords = ["ive", "will", "def", "return", "python", "dont", "u", "f"]
    stopwords = list(stopwords) + additional_stopwords

    # Assuming you have a DataFrame named 'df' with a column named 'text'

    csv_file_path = '/app/Shared/posts_dataframe.csv'
    while not os.path.exists(csv_file_path):
        time.sleep(120)

    df = pd.read_csv(csv_file_path)

    # Solve duplicate column bug
    df = df.drop('Unnamed: 0', axis=1)
    all_words = ''.join([str(string) for string in df['Comments']])

    sentiment_data = df["Insight"].value_counts()

    if st.sidebar.button("Sentiment Chart"):
        generate_chart(sentiment_data)

    if st.sidebar.button("Word Cloud"):
        generate_wordcloud(all_words, stopwords)

    if st.sidebar.button("Comments Data frame"):
        generate_dataframe(df)

    
app = Flask(__name__)

@app.route('/app/channel', methods=["POST"])
def reload_page():
    load_page()


load_page()