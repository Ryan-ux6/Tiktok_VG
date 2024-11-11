import json
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

def caption_video(video_path, subtitle_data):

    # Define a generator function to create text clips for subtitles with a black shadow
    def generator(txt):
        # Create the shadow text clip
        shadow = TextClip(txt, font='Impact', fontsize=88, color='black', stroke_color=None)
        shadow = shadow.set_position(('center', 'center')).set_duration(1)  # Adjust position and opacity

        # Create the main text clip
        main_text = TextClip(txt, font='Impact', fontsize=88, color='white', stroke_color='black', stroke_width=5)

        # Overlay the shadow and main text
        return CompositeVideoClip([shadow.set_position((2, 2)), main_text])  # Adjust shadow position for effect

    # Create a SubtitlesClip using the subtitle data and the text generator
    subtitles = SubtitlesClip(subtitle_data, generator)

    # Load the video file from the given path
    video = VideoFileClip(video_path)

    # Overlay the subtitles on the video, positioning them at the center
    result = CompositeVideoClip([video, subtitles.set_pos(('center'))])

    # Define the output path for the captioned video
    result_path = f'C:/Users/ryana/Documents/VsCode/VideoGenerator/musicaption-master/outputs/captioned_{os.path.basename(video_path)}'

    # Write the final video file with the subtitles, using specified settings
    result.write_videofile(result_path, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == '__main__':
    video_file_name = input('Verify subs.json is okay, then give video file name (exclude ext): ')
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)
    caption_video(f'C:/Users/ryana/Documents/VsCode/VideoGenerator/musicaption-master/inputs/videos/{video_file_name}.mp4', subtitle_data)

print("Successful")