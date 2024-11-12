import json
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

font_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/Montserrat-Black.ttf'


from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip

def add_shadow_layer(video_path, subtitle_data, output_path):
    def shadow_generator(txt):
        txt=txt.upper()
        shadow = TextClip(txt, font=font_path, fontsize=80, color='black', stroke_color=None)
        shadow = shadow.set_opacity(0.5)
        shadow = shadow.set_position((100,100 ))  # Slight offset for shadow effect
        return shadow

    subtitles_shadow = SubtitlesClip(subtitle_data, shadow_generator)
    video = VideoFileClip(video_path)
    result_with_shadow = CompositeVideoClip([video, subtitles_shadow])
    result_with_shadow.write_videofile(output_path, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    
    return output_path

def add_main_text_layer(video_path, subtitle_data, output_path):
    def main_text_generator(txt):
        txt=txt.upper()
        main_text = TextClip(txt, font=font_path, fontsize=80, color='white')
        main_text = main_text.set_opacity(1)
        height = 30 #height of bounce effect
        speed = 2 #speed of bounce effect
        main_text = main_text.set_position(lambda t: ('center', 380 - height * abs(1 - t * speed % 2)))
        return main_text

    subtitles_main = SubtitlesClip(subtitle_data, main_text_generator)
    video = VideoFileClip(video_path)
    result_with_main_text = CompositeVideoClip([video, subtitles_main.set_pos('center')])
    result_with_main_text.write_videofile(output_path, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    
    print(f"Final video with main text layer saved to {output_path}")

# Example usage
if __name__ == '__main__':
    initial_video_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/inputs/videos/video.mp4'  # Path to the original video
    output_path_step1 = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/shadow_video.mp4'
    final_output_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/main_video.mp4'

    # Load subtitle data from JSON file or create it as needed
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)

    # Step 1: Add shadow layer
    shadow_video_path = add_shadow_layer(initial_video_path, subtitle_data, output_path_step1)

    # Step 2: Add main text layer on top of the shadow layer
    add_main_text_layer(shadow_video_path, subtitle_data, final_output_path)





'''    def caption_video(video_path, subtitle_data):

    font_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/Montserrat-Black.ttf'

    # Define a generator function to create text clips for subtitles with a black shadow
    def generator(txt):

        txt=txt.upper()
        
        
        # Create the shadow text clip
        shadow = TextClip(txt, font=font_path, fontsize=50, color='black')
        shadow = shadow.set_position((4,4))  # Slight offset for shadow effect
        shadow = shadow.set_opacity(0.5)  # Adjust opacity

        # Create the main text clip with a bounce effect
        main_text = TextClip(txt, font=font_path, fontsize=50, color='red', stroke_color='white', stroke_width=2)
        height = 30 #height of bounce effect
        speed = 2 #speed of bounce effect
        main_text = main_text.set_position(lambda t: ('center', 380 - height * abs(1 - t * speed % 2)))  # Bounce effect in y-position

        # Overlay the shadow and main text
        return CompositeVideoClip([shadow, main_text])  

    # Create a SubtitlesClip using the subtitle data and the text generator
    subtitles = SubtitlesClip(subtitle_data, generator)

    # Load the video file from the given path
    video = VideoFileClip(video_path)

    # Overlay the subtitles on the video, positioning them at the center
    result = CompositeVideoClip([video, subtitles.set_pos(('center','center'))])

    # Define the output path for the captioned video
    result_path = f'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/captioned_{os.path.basename(video_path)}'

    # Write the final video file with the subtitles, using specified settings
    result.write_videofile(result_path, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    shadow2 = TextClip(subtitle_data, font=font_path, fontsize=50, color='black')
    shadow2 = shadow2.set_position((3,3))  # Slight offset for shadow effect
    shadow2 = shadow2.set_opacity(0.7)  # Adjust opacity


    if __name__ == '__main__':
    video_file_name = input('Verify subs.json is okay, then give video file name (exclude ext): ')
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)
    caption_video(f'C:/Users/ryana/Documents/VsCode/VideoGenerator/musicaption-master/inputs/videos/{video_file_name}.mp4', subtitle_data)

    print("Successful")
    '''