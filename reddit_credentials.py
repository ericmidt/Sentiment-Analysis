import os
from dotenv import load_dotenv

# Setup up IDs and variables from .env local file.
load_dotenv("C:/Python/EnvironmentVariables/.env")
app_name = os.environ.get("reddit_app_name")
app_id = os.environ.get("reddit_app_id")
app_secret = os.environ.get("reddit_app_secret")
app_platform = os.environ.get("reddit_app_platform")
reddit_username = os.environ.get("reddit_username")
reddit_password = os.environ.get("reddit_pw")
USER_AGENT = "windows:" + f"localhost:{app_name}:v1 (by /u/" + reddit_username + ")"

s3_bucket = os.environ.get("s3_reddit_bucket")
