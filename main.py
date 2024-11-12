from moviepy.editor import VideoFileClip, CompositeVideoClip, CompositeAudioClip, TextClip, concatenate_videoclips, AudioFileClip
from PIL import ImageFont
import numpy as np
import os
import importlib.util
import yt_dlp
from subtitles.pre_process_inputs import convert_all_audios_to_wavs
from subtitles.captioner import add_shadow_layer,add_main_text_layer
from subtitles.transcriber import transcribe_to_subs
import json



def download_video(video_url, output_path='subtitles/inputs/videos/video.%(ext)s'):
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

    # Step 3: Running module paths to (Convert to .wav --> Transcribe --> Add Captions)
    # Preprocess the inputs
    os.chdir('subtitles/inputs/audios')
    print(convert_all_audios_to_wavs())
    print("Converting of mp3 to wav was successful")

    # Transcribe the audio
    #use_existing = input('Use existing subs.json file (y/n)? ')
    #if use_existing == 'n':
        #audio_file_name = input('Audio file name (exclude ext): ')
    wav_path="C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/inputs/audios/voiceover.wav"
    transcribe_to_subs(wav_path)
    #else:
    #    print('Using current subs.json')
    #print("Transcription was succesful")

    # Add captions to the video
    #video_file_name = input('Verify subs.json is okay, then give video file name (exclude ext): ')
    initial_video_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/inputs/videos/video.mp4'  # Path to the original video
    output_path_step1 = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/shadow_video.mp4'
    final_output_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/final/main_video.mp4'

    # Load subtitle data from JSON file or create it as needed
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)

    # Step 1: Add shadow layer
    shadow_video_path = add_shadow_layer(initial_video_path, subtitle_data, output_path_step1)

    # Step 2: Add main text layer on top of the shadow layer
    add_main_text_layer(shadow_video_path, subtitle_data, final_output_path)

    # Step 4: Combine video and voiceover files
    video_clip = VideoFileClip(final_output_path)
    audio_clip = AudioFileClip("C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/inputs/audios/voiceover.wav")


    video_clip=video_clip.set_audio(audio_clip)    
    # final_clip.write_videofile(output_path, fps=video_clip.fps)
    
    video_clip = video_clip.subclip(0, min(video_clip.duration, audio_clip.duration))

    # Step 5: Save the final video
    video_clip.write_videofile("C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/final/final_video.mp4")
    print("Final brainrot video has been created successfully.")


# Example Usage
if __name__ == "__main__":
    script = "This is a sample script. It will be converted into a voiceover. Captions will also be added to the video."
    video_link = "https://www.youtube.com/watch?v=_Td7JjCTfyc"  # Replace with any YouTube link or local video path
    process_brainrot_video(script, video_link)
