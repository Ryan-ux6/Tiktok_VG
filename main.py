from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, concatenate_videoclips, AudioFileClip
from PIL import ImageFont
import numpy as np
import os
from subtitles import pre_process_inputs
from subtitles import transcriber
from subtitles import captioner
import importlib.util
import yt_dlp



def download_video(video_url, output_path='subtitles/inputs/video/video.%(ext)s'):
    """Downloads a video from YouTube using yt-dlp."""
    ydl_opts = {'format': 'bestvideo[ext=mp4]',
                'outtmpl': output_path}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(result)            
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    print(filename)
    return filename


def generate_voiceover(script_text, output_path):
    """Generates a voiceover from the given script using pyttsx3."""
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)  # Set speech rate to slow  down the voice
    engine.setProperty('voice', 'male')  # Set voice to male
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    engine.save_to_file(script_text, output_path)
    engine.runAndWait()
    return output_path

def load_and_run_module(module_name, file_path):
    """Loads and executes a module from the given file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is not None and spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        print(f"Error: Could not find or load the module '{module_name}'.")


def process_brainrot_video(script_text, video_source, output_path='final_brainrot_video.mp4'):
    """Processes the video to add voiceover and captions."""
    # Step 1: Download video if a link is provided
    if video_source.startswith("http"):
        video_source = download_video(video_source)
        if video_source is None:
            print("Failed to download video.")
            return

    # Step 2: Generate voiceover
    voiceover_path = generate_voiceover(script_text, output_path="subtitles/inputs/audios/voiceover.mp3")
    if voiceover_path is None:
        print("Failed to generate voiceover.")
        return

    # Step 3: Assigning module paths to (Convert to .wav --> Transcribe --> Add Captions)
    pre_process_path = os.path.join(os.path.dirname(__file__), 'subtitles', 'pre_process_inputs.py')
    transcriber_path = os.path.join(os.path.dirname(__file__), 'subtitles', 'transcriber.py')
    captioner_path = os.path.join(os.path.dirname(__file__), 'subtitles', 'captioner.py')

    # Step 4: Converting voiceover audio files to .wav format
    load_and_run_module("pre_process_inputs", pre_process_path)

    # Step 5: Transcribe the audio
    load_and_run_module("transcriber", transcriber_path)

    # Step 6: Add captions to the video
    load_and_run_module("captioner", captioner_path)


# Example Usage
if __name__ == "__main__":
    script = "This is a sample script. It will be converted into a voiceover. Captions will also be added to the video."
    video_link = "https://www.youtube.com/watch?v=_Td7JjCTfyc"  # Replace with any YouTube link or local video path
    process_brainrot_video(script, video_link)
