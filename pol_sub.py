from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

#Create a function to get the subjectivity
def getSubjectivity(text):
 return TextBlob(text).sentiment.subjectivity

#Create a function to get Polarity
def getPolarity(text):
 return TextBlob(text).sentiment.polarity

