# from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
import requests
import time


while True:
    filepath = '/app/Shared/channel_name.txt'
    while not os.path.exists(filepath):
        print("Waiting channel name...")
        time.sleep(1)

    print("Channel name found... \nProcessing...")
    # api_key = os.getenv("youtube_api_key")
    api_key = "AIzaSyBr0k4vrmqosOglckneJBoIOVQQ2qezDw8"

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    with open(filepath, 'r') as file:
        custom_username = file.read()

    # Get channel ID from custom username
    response = youtube.search().list(part='id', q=custom_username, type='channel').execute()

    # Extract the channel ID from the response
    channel_id = response['items'][0]['id']['channelId']

    # Get the last 10 videos of the channel
    response = youtube.search().list(part='snippet', channelId=channel_id, maxResults=10, order='date').execute()
    videos = response['items']

    # Initialize an empty dictionary to store the video titles and comments
    data = []

    # Get the top 100 comments from each video and store them in the dictionary
    for video in videos:
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']

        response = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults=50, order='relevance').execute()
        comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
        # Add comments to data
        data.extend(comments)

    ### Uses a json file to send comments data to the Processing container's API ###
    filename = '/app/Shared/reddit_data.json'
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Pretty print with indent=4
        print(f"Data saved at {filename}") 

    url = "http://data_preprocessing:5000/app/data"
    flask_data = {"filepath": filename}
    response = requests.post(url=url, json=flask_data)

    if response.status_code == 200:
        print("Data sent successfully to the data processing container.")
    else:
        print(response.status_code, " Error sending data to the data processing container.")

    os.remove(filepath)
    time.sleep(0.5)