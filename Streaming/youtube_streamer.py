# from dotenv import load_dotenv
from googleapiclient.discovery import build
import json
from flask import Flask, request
import os
import requests

app = Flask(__name__)

def get_comments(channel_name):

    api_key = "AIzaSyDVfnlpeKf_VCKrBzMbslw-uvGy9HAm7HQ"

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get channel ID from custom username
    custom_username = channel_name
    response = youtube.search().list(part='id', q=custom_username, type='channel').execute()
    total_results = response['pageInfo']['totalResults']
    # If there are no search results for the channel name
    if total_results <=0:
        return -1
    
    # Extract the channel ID from the response
    channel_id = response['items'][0]['id']['channelId']

    # Get the last 10 videos of the channel
    response = youtube.search().list(part='snippet', channelId=channel_id, maxResults=10, order='date').execute()
    videos = response['items']

    # Initialize an empty list to store the comments
    data = []

    # Get the top 100 comments from each video and store them in the dictionary
    for video in videos:
        video_id = video['id']['videoId']
        response = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults=50, order='relevance').execute()
        comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
        # Add comments to data
        data.extend(comments)
    return data


def send_comments_to_data_preprocessing(data):
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


def send_channel_name_to_streamlit(channel_name):
    ### Uses a txt file to send the channel name to the Streamlit container's API ###
    # Save the channel name to a .txt file
    txt_filename = '/app/Shared/channel_name.txt'

    with open(txt_filename, 'w') as txt_file:
        txt_file.write(channel_name)
        print(f"Channel name saved at {txt_filename}")

    url = "http://front_streamlit:8501/app/channel"
    flask_data = {"filepath": txt_filename}

    # Send an HTTP POST request with the channel name file
    response = requests.post(url=url, json=flask_data)

    if response.status_code == 200:
        print("Channel name sent successfully to the streamlit container.")
    else:
        print(response.status_code, " Error sending channel name to the streamlit container.")


def teste():    
    file_path = '/app/Shared/channel_name.json'
    if os.path.exists(file_path):

        channel_name = request.json
        file_path = channel_name.get("filepath")

        # Update the channel name in the channel_name.txt file
        with open(file_path, 'r') as json_file:
            data =json.load(json_file)

        comments = get_comments(data)
        if comments == -1:
            return "Invalid channel name."
        else:
            send_comments_to_data_preprocessing(comments)
            send_channel_name_to_streamlit(data)
            return 'Channel name updated successfully.'

    else:
        comments = get_comments("fireship")
        send_comments_to_data_preprocessing(comments)
        send_channel_name_to_streamlit("fireship")
        
streamer = True
teste()
while streamer:
    @app.route('/app/data', methods=['POST'])
    def update_channel_name():
        teste()
