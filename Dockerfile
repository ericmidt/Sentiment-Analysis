FROM python:3.11

WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["sh", "-c", "python reddit_streamer.py && python data_preprocessing.py && streamlit run --server.port=8501 --server.address=0.0.0.0 front_streamlit.py"]

#ENTRYPOINT ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0"]

#CMD ["python", "reddit_streamer.py", "data_preprocessing.py", "front_streamlit.py"]