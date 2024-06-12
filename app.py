from fastapi import FastAPI, Request
from starlette.responses import FileResponse
import os
import pandas as pd
import moviepy.editor as mp
import torch
import random
from uuid import uuid4 


from services.download_video import download_youtube_video
from services.text_to_speech import text_to_en_speech
from services.create_video import create_video


# Initialize FastAPI application
app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
tts_model = "tts_models/multilingual/multi-dataset/xtts_v2"

@app.post("/download-video")
async def download_video(request: Request):
    json_data = await request.json()
    youtube_url = json_data.get("yt_url")

    if "csv_file" in json_data:
        csv_file = json_data["csv_file"]
    else:
        csv_file = "csv_data/data.csv"
    
    file_path = download_youtube_video(youtube_url,"videos")    
    
    # Define the directory path
    dir_path = os.path.dirname(csv_file)

    # Check if the directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)     
        print(f'Directory {dir_path} created successfully.')
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file, encoding="utf-8")
    else:
        data = pd.DataFrame(columns=['video_path', 'last_second',"duration"])
    if file_path in data["video_path"].values:
        return "video already exist"
    else:
        clip = mp.VideoFileClip(file_path)
        new_data = {'video_path': file_path, 'last_second': 15, "duration": clip.duration}
        data = data.append(new_data, ignore_index=True)
        data.to_csv(csv_file, index=False, encoding='utf-8')
        return {"video_path":file_path}

@app.post("/create-video")
async def create_reel(request: Request):
    json_data = await request.json()
    if "speaker_wav" in json_data:
        speaker_wav = json_data["speaker_wav"]
    else:
        speaker_wav = "audio/morgan_audio.wav"
    quote = json_data.get("quote")

    output_video_path = f"videos/{str(uuid4())}.mp4"

    temp_wav_path = text_to_en_speech(tts_model, device, quote, speaker_wav)
    temp_wav_path = "temp.wav"
    audio_clip = mp.AudioFileClip(temp_wav_path)
    audio_duration = audio_clip.duration
    print("duration============",audio_duration)
    data = pd.read_csv("./csv_data/data.csv")
    i = random.choice(range(len(data)))
    while data.loc[i,"duration"] - data.loc[i,"last_second"]-5<audio_duration:
        data = data.drop(index=i)
        data = data.reset_index(drop=True)
        i = random.choice(range(len(data)))
    data.loc[i,"last_second"]+= audio_duration
    data.to_csv("./csv_data/data.csv",index=False)
    create_video(data.loc[i,"video_path"], temp_wav_path, output_video_path, data.loc[i,"last_second"])
    # os.remove(temp_wav_path)
    return "Done" 



