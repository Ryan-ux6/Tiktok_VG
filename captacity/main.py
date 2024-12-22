import os
import subprocess
import sys
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
# from moviepy.audio.AudioClip import AudioFileClip
import pyttsx3
from transformers import pipeline
import captacity
# from TTS.api import TTS




CURRENT_DIR = os.getcwd()

# Constants
INP_FILE_NAME = "something.mp4"
OUT_FILE_NAME = "output.mp4"
FONT = "Montserrat-ExtraBold.ttf"
DEFAULT_PHONE_SIZE = (1080, 1920)  # Typical phone screen size (width x height)

def download_youtube_video(youtube_url, save_path):
    output_file = os.path.join(save_path, "downloaded_video.mp4")
    command = [
        "yt-dlp",
        "-f", "mp4",
        youtube_url,
        "-o", output_file
    ]
    subprocess.run(command, check=True)
    return output_file

def crop_to_phone_size(video_path, output_path, phone_size=DEFAULT_PHONE_SIZE):
    video = VideoFileClip(video_path)
    width, height = video.size
    if width != phone_size[0] or height != phone_size[1]:
        cropped_video = video.crop(width=phone_size[0], height=phone_size[1], x_center=width//2, y_center=height//2)
    else:
        cropped_video = video
    cropped_video.write_videofile(output_path, codec="libx264")
    return output_path

def generate_voiceover(text, output_audio_file):
    engine = pyttsx3.init()
    # Configure the voice to be male
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 for male voice
    engine.setProperty('rate', 150)  # Adjust speaking speed
    engine.setProperty('volume', 0.9)  # Set volume
    # Save the audio
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()
    return output_audio_file

def combine_video_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec="libx264")
    return output_path

if __name__ == "__main__":
    # Take YouTube link and download video
    youtube_url = "https://www.youtube.com/watch?v=RbVMiu4ubT0" # input("Enter the YouTube video link: ")
    downloaded_video = download_youtube_video(youtube_url, save_path=os.path.join(CURRENT_DIR, "assets/content/input/video"))
    
    # Ensure the video is cropped to phone size
    cropped_video_path = os.path.join(CURRENT_DIR, "assets/content/input/video/cropped_video.mp4")
    cropped_video = crop_to_phone_size(downloaded_video, cropped_video_path)

    # Generate voiceover for input text
    voiceover_text = "This is a sample voiceover. It has multiple lines all over" #input("Enter the text for the voiceover: ")
    voiceover_audio_path = os.path.join(CURRENT_DIR, "assets/content/input/audio/voiceover.mp3")
    generate_voiceover(voiceover_text, voiceover_audio_path)

    # Combine the video and audio
    combined_video_path = os.path.join(CURRENT_DIR, "assets/content/input/video/combined_video.mp4")
    combine_video_audio(cropped_video, voiceover_audio_path, combined_video_path)

    # Run the captioning process
    captacity.add_captions(
        video_file=combined_video_path,
        output_file=os.path.join(CURRENT_DIR, f"assets/content/output/{OUT_FILE_NAME}"),
        font= "C:/Users/HP/Desktop/2024/Extra/VideoGenerator/Ryan/Tiktok_VG/captacity/assets/fonts/Montserrat-ExtraBold.ttf", #os.path.join(CURRENT_DIR, f"assets/fonts/{FONT}"),
        font_size=40,
        font_color="white",
        stroke_width=.5,
        stroke_color="black",
        shadow_strength=10,
        shadow_blur=10,
        highlight_current_word=True,
        word_highlight_color="yellow",
        line_count=1,
        padding=50,
    )

    # Display a message when execution is complete
    print("Captioning process complete! The output video has been saved.")
