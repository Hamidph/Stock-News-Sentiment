# -*- coding: utf-8 -*-
"""YoutubeChannelsData.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uRTV1mF10wnJ0x6i8KmrNVMnX78auPyY
"""

pip install google-api-python-client

!pip install transformers
!pip install youtube-transcript-api
!pip install pytube
import pandas as pd
import matplotlib.pyplot as plt
from pytube import YouTube
import requests

from googleapiclient.discovery import build

api_key = 'AIzaSyAhKIAd0PBKzZlblVi2VVddxxYq8HubrIA' # Replace with your actual API key
#second AIzaSyAhKIAd0PBKzZlblVi2VVddxxYq8HubrIA
#first  AIzaSyAzGUexMj_4X_JJEiVBv3vMuAZPJrbxMSc
# Build the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


# Function to get the Channel ID from a video URL
def yt_id(url):
    yt = YouTube(url)
    channel_id = yt.channel_id
    return channel_id

# Creating a list of videos from channels I want data from
videos = [
    #'https://youtu.be/rQM8Pv9BSHM?si=T-J7eMhYS6xZJ_LI',
    #'https://youtu.be/g2ochnq6-ds?si=8O3xz6NW2izvDTWB',
   #'https://youtu.be/0ZbgTDVUiE8?si=LOxmlxgNG6vaRAF8',
    #'https://youtu.be/_7Ii3t957d4?si=uU4Q4GBBySANpAml',
   #'https://youtu.be/Kj1HSQByQ8A?si=W_mFidKQYfSUo9-a',
    #'https://youtu.be/JLzsBbkeEm8?si=U_gQqcW_42JYmuI_',
   #'https://youtu.be/GOVE5oR0jJ8?si=HqX0qZouYSVWCMSZ',
    #'https://youtu.be/2vUQyisVmng?si=aI5Q6IrW09z-DBb0',
    #'https://youtu.be/x2FOvtEa0h0?si=8Qgb5PSnQwur0RYr',
    #'https://youtu.be/xaFJWhuiRas?si=7Gk4KZDuLVnFREeA',
    'https://youtu.be/EC3CCt3NXWc?si=MN1LDeDv9BzTUjDd',
    'https://youtu.be/Vh9xhdIfMjY?si=Ui5zVpnRprl1WvcA'


]

# This for loop will iterate through each video, use both functions to grab data
channel_ids = []
for video in videos:
    id = yt_id(video)
    channel_ids.append(id)

# Print the Channel IDs
print(channel_ids)

# Define your YouTube API key
key = 'AIzaSyAhKIAd0PBKzZlblVi2VVddxxYq8HubrIA'  # Replace with your actual YouTube API key

# Date range for filtering videos (May 1, 2024, to May 31, 2024)
start_date = '2022-06-01T00:00:00Z'
end_date = '2024-06-30T23:59:59Z'

# Function to get the video transcript
def get_video_transcript(video_id):
    try:
        # Fetch the transcript for the video
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Join the transcript parts into a single string
        transcript = ' '.join([item['text'] for item in transcript_list])
    except (TranscriptsDisabled, NoTranscriptFound):
        transcript = "Transcript not available"
    except Exception as e:
        transcript = f"Error retrieving transcript: {e}"
    return transcript

# Function to get all videos from a channel using pagination
def get_channel_data(key, channel_id):
    youtube = build('youtube', 'v3', developerKey=key)
    channel_data = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            key=key,
            channelId=channel_id,
            part='snippet',
            order='date',
            publishedAfter=start_date,
            publishedBefore=end_date,
            maxResults=50,  # Max results per page
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                publish = item['snippet']['publishedAt']
                title = item['snippet']['title']
                description = item['snippet']['description']
                channel_name = item['snippet']['channelTitle']

                # Get the transcript for the video
                transcript = get_video_transcript(video_id)

                video_info = {
                    'publish': publish,
                    'title': title,
                    'description': description,
                    'channel_name': channel_name,
                    'transcript': transcript
                }

                channel_data.append(video_info)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    df = pd.DataFrame(channel_data)
    return df

# Get channel information for each channel
meet_kevin = get_channel_data(key, channel_ids[0])
bloomberg = get_channel_data(key, channel_ids[1])

# Combine all of the data frames together into one
df = pd.concat([meet_kevin, bloomberg])
df = df.reset_index(drop=True)

# Print the resulting DataFrame
print(df)

# Sorting by 'publish' column in descending order
sorted_df_desc = df.sort_values(by='publish', ascending=False)
# Save DataFrame to an Excel file
df.to_excel('may4.xlsx', index=False)
df.head(3)

# ... (rest of your code)

# Print the resulting DataFrame
print(df)

# Save the DataFrame to an Excel file
df.to_excel("youtube_data_oney.xlsx", index=False)