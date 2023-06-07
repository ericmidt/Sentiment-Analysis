FROM python:3.11

WORKDIR /app

# Creates a Python virtual environment (venv) at the /venv directory inside the container
RUN python -m venv /venv
# Sets an environment variable named PATH to include the /venv/bin directory.
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["sh", "-c", "python reddit_streamer.py && python data_preprocessing.py && streamlit run --server.port=8501 --server.address=0.0.0.0 front_streamlit.py"]
