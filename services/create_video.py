import cv2
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import tempfile


def create_video(video_path, audio_path, output_video_path, start_second):
    video_clip = mp.VideoFileClip(video_path)

    # Get the frame rate of the original video
    fps  = video_clip.fps

    # Load the new audio using MoviePy
    new_audio_clip = mp.AudioFileClip(audio_path)

    # Get the duration of the new audio clip
    new_audio_duration = new_audio_clip.duration

    subclip = video_clip.subclip(start_second, start_second + new_audio_duration)

    # Ensure the new audio clip has the same duration as the video
    new_audio_clip = new_audio_clip.set_duration(float(new_audio_duration))

    # Replace the audio of the video clip with the new audio
    subclip = subclip.set_audio(new_audio_clip)

    # Resize the video to the reel size
    clip_resized = subclip.resize(height=1920)
    clip_cropped = clip_resized.crop(width=1080, height=1920, x_center=clip_resized.w/2, y_center=clip_resized.h/2)


    # Write the final video with the new audio
    clip_cropped.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=fps)

    print("The video with the new audio has been saved to:", output_video_path)