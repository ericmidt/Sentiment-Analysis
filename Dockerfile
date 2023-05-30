FROM python:latest

WORKDIR /app

COPY README.md ./
COPY front_streamlit.py ./
COPY pol_sub.py ./
COPY reddit_credentials.py ./
COPY reddit_streamer.py ./
COPY data_preprocessing.py ./
COPY requirements.txt ./

RUN apt-get -y update && apt-get install -y python

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "front_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]