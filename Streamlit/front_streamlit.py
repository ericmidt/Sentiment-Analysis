import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time
import os

# Cancel warning in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Youtube Sentiment Analysis")

# Create sidebar
st.sidebar.header("Youtube Channel Sentinment Analysis")
st.sidebar.subheader("Options")

# Read the channel name from the .txt file

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


channel = st.sidebar.text_input("Type Youtube Channel:")
filepath = '/app/Shared/channel_name.txt'

if st.sidebar.button("Save Channel") and channel:

    with open(filepath, 'w') as file:
        file.write(channel)
        print("Saved")
    st.sidebar.success(f"Channel '{channel}' saved successfully!")