FROM python:latest

WORKDIR /app

COPY . .

RUN apt-get -y update && apt-get install -y python

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run","reddit_streamer.py", "data_preprocessing.py", "front_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]