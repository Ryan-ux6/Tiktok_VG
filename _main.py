from subtitles.pre_process_inputs import convert_all_audios_to_wavs
from subtitles.captioner import caption_video
from subtitles.transcriber import transcribe_to_subs
import os
import json
import yt_dlp
import pyttsx3


def generate_voiceover_from_script(script_text, output_path='inputs/audios/voiceover.wav'):
    """Generates a voiceover from the given script using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)  # Adjust speech rate as needed
    engine.setProperty('voice', 'male')  # Set to male voice (if available)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save voiceover to the specified path
    engine.save_to_file(script_text, output_path)
    engine.runAndWait()
    return output_path


def download_video(video_url="https://www.youtube.com/watch?v=tVWZOs48DNg", output_path='subtitles/inputs/videos/video1.mp4'):
    """Downloads a video from YouTube using yt-dlp."""
    ydl_opts = {'format': 'bestvideo+bestaudio[ext=mp4]',  # Download video and audio best quality
                'outtmpl': output_path}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(result)            
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    print(f"Downloaded video saved as: {filename}")
    return filename


def generate_subtitles(video_path, url="https://www.youtube.com/watch?v=tVWZOs48DNg", audio_path=None, script_text=None, language='en'):
    # Generate or use an existing audio file
    if script_text:
        # Generate voiceover from the script and set as the audio path
        audio_path = generate_voiceover_from_script(script_text)
    elif audio_path:
        # If an audio path is provided, convert it to .wav format
        os.makedirs('inputs/audios', exist_ok=True)
        convert_all_audios_to_wavs()
        audio_file_name = os.path.splitext(os.path.basename(audio_path))[0]
        audio_path = f'inputs/audios/{audio_file_name}.wav'
    
    # Transcribe the audio to subtitles
    transcribe_to_subs(audio_path)

    # Add captions to the video
    video_file_name = download_video(video_url=url)  # Downloads video to specified path
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)
    
    # Generate the final video with captions
    caption_video(f'{video_file_name}', subtitle_data)


if __name__ == '__main__':
    # Example usage: provide script_text instead of an audio file
    video_path = "subtitles/outputs/"  # Specify output directory
    script_text = "This is a sample voiceover. It has no actual text."
    generate_subtitles(video_path, script_text=script_text)
