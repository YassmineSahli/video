import os
import requests
from urllib.parse import unquote
from pytube import YouTube




def download_video(url,download_folder):
    """
    Download video from the given URL.

    Args:
        url (str): The URL of the video to download.

    Returns:
        tuple: A tuple containing the file path of the downloaded video and its title.
               Returns (None, None) if the download fails.
    """

    response = requests.get(url)
    if response.status_code == 200:
        # Extract video name from URL
        video_name = os.path.basename(unquote(url))
        video_name, _ = os.path.splitext(video_name)
        
        # Determine video file extension
        content_type = response.headers.get('content-type')
        if 'video/mp4' in content_type:
            video_extension = '.mp4'
        elif 'video/quicktime' in content_type:
            video_extension = '.mov'
        else:
            print("Unsupported video format")
            return None, None
        
        file_path = os.path.join(download_folder, f"{video_name}{video_extension}")
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path, video_name
    else:
        return None, None

def download_youtube_video(video_url,download_folder):
    video_name = os.path.basename(unquote(video_url))
    video_name, _ = os.path.splitext(video_name)
    yt = YouTube(video_url)

    # Get the highest resolution stream available
    stream = yt.streams.get_highest_resolution()
    filepath = f'{download_folder}/{video_name}.mp4'
    # Download the video
    stream.download(output_path='.', filename=filepath)
    return filepath