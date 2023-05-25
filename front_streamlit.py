import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import data_preprocessing

# Cancel warning in streamlit
st.set_option('deprecation.showPyplotGlobalUse', False)

def generate_wordcloud(data, stopwords_list):
    wordcloud = WordCloud(width=800, height=400, background_color='black', max_words=100, stopwords=stopwords_list).generate(data)
    st.title("Word Cloud")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

def generate_chart(data):
    pass


stopwords = STOPWORDS
stopwords.add("ive")
stopwords.add("will")
stopwords.add("def")
stopwords.add("return")
stopwords.add("python")
stopwords.add("dont")
stopwords.add("u") 
# Assuming you have a DataFrame named 'df' with a column named 'text'
df = pd.read_csv('posts_dataframe.csv')
all_words = ''.join([str(string) for string in df['Posts']])

""" print(df["Insight"].value_counts()) """


if st.button("Generate Word Cloud"):
    generate_wordcloud(all_words, stopwords)

