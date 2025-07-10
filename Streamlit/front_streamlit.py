import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time
import os

# Cancel warning in streamlit
#st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Youtube Sentiment Analysis")

# Create sidebar
st.sidebar.header("Youtube Channel Sentiment Analysis")
st.sidebar.subheader("Options")

def generate_wordcloud(data, stopwords_list):
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, stopwords=stopwords_list).generate(data)
    st.title("Word Cloud")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def generate_chart(data):
    st.title("Sentiment Chart")
    fig, ax = plt.subplots()
    data.plot(kind='bar', ax=ax)
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of posts")
    st.pyplot(fig)

def generate_dataframe(data):
    st.title("Comments Data Frame")
    st.dataframe(data)

stopwords = STOPWORDS
additional_stopwords = ["ive", "will", "def", "return", "python", "dont", "u", "f"]
stopwords = list(stopwords) + additional_stopwords

# Assuming you have a DataFrame named 'df' with a column named 'text'

csv_file_path = '/app/Shared/posts_dataframe.csv'

if os.path.exists(csv_file_path):
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
else:
    st.info("No data available yet. Please enter a channel and save it to start the process.")


channel = st.sidebar.text_input("Type Youtube Channel:")
filepath = '/app/Shared/channel_name.txt'

if st.sidebar.button("Save Channel") and channel:

    with open(filepath, 'w') as file:
        file.write(channel)
        print("Saved")
    st.sidebar.success(f"Channel '{channel}' saved successfully!")