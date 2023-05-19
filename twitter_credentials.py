import os
from dotenv import load_dotenv

# Loads environment variables from .env local file.
load_dotenv("C:/Python/EnvironmentVariables/.env")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
