import os
from flask import Flask, request, render_template, send_file
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import yt_dlp
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pyttsx3

app = Flask(__name__)

def download_video(video_url, output_filename='downloaded_video.mp4'):
    """Downloads a video from YouTube using yt-dlp."""
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'mp4'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    return output_filename

def generate_voiceover(script_text, output_file='voiceover.mp3'):
    """Generates a voiceover from the given script using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate to slow down the voice
    engine.setProperty('voice', 'male')  # Set voice to male
    engine.save_to_file(script_text, output_file)
    engine.runAndWait()
    return output_file

def add_voiceover_to_video(video_path, audio_path, output_path='video_with_voice.mp4'):
    """Adds a voiceover audio track to the video."""
    try:
        video_clip = VideoFileClip(video_path)
    except OSError as e:
        print(f"Error loading video file: {e}")
        return None
    audio_clip = AudioFileClip(audio_path)
    
    # Trim the video to match the length of the audio
    video_clip = video_clip.subclip(0, min(video_clip.duration, audio_clip.duration))
    
    # Set audio to the video
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, threads=4, fps=24, remove_temp=True)
    return output_path

def add_captions(video_path, script_text, output_path='captioned_video.mp4'):
    """Adds captions to the video based on the given script using PIL."""
    try:
        video_clip = VideoFileClip(video_path)
    except OSError as e:
        print(f"Error loading video file: {e}")
        return None
    duration = video_clip.duration
    
    # Split the script by sentences or lines
    lines = script_text.split('. ')
    clips = []

    # Calculate start times and duration for each caption
    caption_duration = duration / len(lines)

    # Add each line as a text clip to the video
    for i, line in enumerate(lines):
        # Create an image with PIL
        img = Image.new('RGBA', video_clip.size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Set font - replace with a valid font path on your system if needed
        try:
            font = ImageFont.truetype("Montserrat-Regular.ttf", 36)
        except IOError:
            font = ImageFont.load_default()
            # Add text with border to the image
        # Add text to the image
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        text_x = (img.width - text_width) / 2
        text_y = img.height - text_height - 50  # Position at the bottom of the video

        border_size = 2
        for x_offset in [-border_size, 0, border_size]:
            for y_offset in [-border_size, 0, border_size]:
                if x_offset != 0 or y_offset != 0:
                    draw.text((text_x + x_offset, text_y + y_offset), line, font=font, fill="black")
        draw.text((text_x, text_y), line, font=font, fill="white")
        # Convert the image to a numpy array and create a moviepy ImageClip
        img_np = np.array(img)
        text_clip = ImageClip(img_np, duration=caption_duration)
        text_clip = text_clip.set_position(('center', 'bottom')).set_start(i * caption_duration)
        
        # TODO: Add a bouncy effect to the text clip
        # text_clip = text_clip.set_position(lambda t: ('center', 'middle' if t < 0.5 else 'middle' + str(10 * np.sin(2 * np.pi * t))))
        
        clips.append(text_clip)

    # Combine text clips with the original video
    final_clip = CompositeVideoClip([video_clip, *clips])
    final_clip = final_clip.set_audio(video_clip.audio)  # Ensure audio is retained
    final_clip.write_videofile(output_path, threads=4, fps=24, remove_temp=True)
    return output_path

def process_brainrot_video(script_text, video_source, output_path='static/final_brainrot_video.mp4'):
    """Processes the video to add voiceover and captions."""
    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
    # Step 1: Download video if a link is provided
    if video_source.startswith("http"):
        video_source = download_video(video_source)
        if video_source is None:
            print("Failed to download video.")
            return None

    # Step 2: Generate voiceover
    voiceover_path = generate_voiceover(script_text)

    # Step 3: Add voiceover to video
    video_with_voice_path = add_voiceover_to_video(video_source, voiceover_path)
    if video_with_voice_path is None:
        print("Failed to add voiceover to video.")
        return None

    # Step 4: Add captions to video
    final_video_path = add_captions(video_with_voice_path, script_text, output_path)
    if final_video_path is None:
        print("Failed to add captions to video.")
        return None

    return final_video_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        script = request.form['script']
        video_link = request.form['video_link']

        # Process the video
        output_path = 'static/final_brainrot_video.mp4'
        final_video_path = process_brainrot_video(script, video_link, output_path)

        if final_video_path is None:
            return "Failed to process the video. Please check the inputs and try again."

        return render_template('index.html', video_url=final_video_path)
    
    return render_template('index.html', video_url=None, status_message='Idle')

@app.route('/download')
def download():
    path = "static/final_brainrot_video.mp4"
    return send_file(path, as_attachment=True)

@app.route('/clear_all', methods=['POST'])
def clear_all():
    """Clears all generated mp3, mp4, and webm files."""
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.mp3', '.mp4', '.webm')):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")
    return """
        All files cleared successfully.<br>
        <a href="/">Return to Home Page</a>
    """

@app.route('/status', methods=['GET'])
def status():
    global status_message
    return jsonify({'status': status_message})


if __name__ == "__main__":
    app.run(debug=True)
