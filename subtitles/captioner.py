import json
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

font_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/Montserrat-Black.ttf'


from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
HEIGHT = 0 #HEIGHT of bounce effect
SHADOW_HEIGHT = -HEIGHT + 5
SPEED = 20 #SPEED of bounce effect
OFFSET = 2

SHADOW_OFFSET_X = 50
SHADOW_OFFSET_Y = 30
def add_shadow_layer(video_path, subtitle_data, output_path):
    def shadow_generator(txt):
        txt=txt.upper()
        shadow = TextClip(txt, font=font_path, fontsize=84, color='black', stroke_color=None)
        shadow = shadow.set_opacity(0.95)
        return shadow

    subtitles_shadow = SubtitlesClip(subtitle_data, shadow_generator)
    video = VideoFileClip(video_path)
    #result_with_shadow = CompositeVideoClip([video, subtitles_shadow.set_position('center', 'center')])
    result_with_shadow = CompositeVideoClip([video, subtitles_shadow.set_position((video.w/2,video.h/2))])
    print(video.w, "+", video.h)
    result_with_shadow.write_videofile(output_path, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    
    return output_path


def add_main_text_layer(video_path, subtitle_data, output_path):
    def main_text_generator(txt):
        txt=txt.upper()
        main_text = TextClip(txt, font=font_path, fontsize=60, color='white')
        main_text = main_text.set_opacity(1)
        return main_text


    
    subtitles_main = SubtitlesClip(subtitle_data, main_text_generator)
    # subtitles_shadow = SubtitlesClip(subtitle_data, shadow_text_generator)
    video = VideoFileClip(video_path)
    # result_with_main_text = CompositeVideoClip([video, subtitles_main.set_position(('center', 'center'))])
    # lambda t: ('center', 380 - HEIGHT * abs(1 - t * SPEED % 2))
    result_with_main_text = CompositeVideoClip([video, subtitles_main.set_position((video.w/2,video.h/2))])
    # result_with_main_text = CompositeVideoClip([result_with_main_text, subtitles_shadow.set_pos('center')])
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
    # add_shadow_text_layer(final_output_path, subtitle_data, final_output_path)
    add_main_text_layer(shadow_video_path,subtitle_data, final_output_path)

'''
    if __name__ == '__main__':
    video_file_name = input('Verify subs.json is okay, then give video file name (exclude ext): ')
    with open('./subs.json', 'r') as f:
        subtitle_data = json.load(f)
    caption_video(f'C:/Users/ryana/Documents/VsCode/VideoGenerator/musicaption-master/inputs/videos/{video_file_name}.mp4', subtitle_data)

    print("Successful")
    '''