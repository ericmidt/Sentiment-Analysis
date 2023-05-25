import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import data_preprocessing


st.write("Bling bling pa pling")
st.write(data_preprocessing.dataframe)

def generate_wordcloud(data):
    text = ' '.join(data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

def main():
    st.title("Word Cloud Generator")
    
    # Assuming you have a DataFrame named 'df' with a column named 'text'
    df = pd.read_csv('posts_dataframe.csv')
    
    st.dataframe(df)  # Display the DataFrame in Streamlit
    
    selected_rows = st.multiselect("Select rows", df.index.tolist())
    selected_data = df.loc[selected_rows, 'Posts']
    
    if st.button("Generate Word Cloud"):
        generate_wordcloud(selected_data)

if __name__ == '__main__':
    main()
