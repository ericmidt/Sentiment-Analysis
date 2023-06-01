import os
from dotenv import load_dotenv

# Setup up IDs and variables from .env local file.
#load_dotenv("C:/Python/EnvironmentVariables/.env")
app_name = "sent_analysis_br"
app_id = "qURatL5KzO7NYjJrehM_uw"
app_secret = "WQHmtHM_NT0U3DfpHW3IS5XltWTelA"
app_platform = "script"
reddit_username = "FlingoLingo_Potato"
reddit_pw = "Garagem9@"
USER_AGENT = "windows:" + f"localhost:{app_name}:v1 (by /u/" + reddit_username + ")"

s3_bucket = os.environ.get("s3_reddit_bucket")
