import json
import os
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

# Define font path
main_font_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/midroba.regular.ttf'
shadow_font_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/midroba.schatten.ttf'

# Shadow configuration
SHADOW_OFFSET = (2, 2)      # (x, y) offset for shadow in pixels
SHADOW_OPACITY = 0.6        # Opacity for shadow text
SHADOW_FONT_SIZE = 60       # Reduced font size for shadow


# Main text configuration
MAIN_TEXT_COLOR = 'white'
MAIN_FONT_SIZE = 60         # Font size for main text

def shadow_generator(txt):
    txt = txt.upper()
    shadow = TextClip(txt, font=shadow_font_path, fontsize=SHADOW_FONT_SIZE, color='black')
    shadow = shadow.set_opacity(SHADOW_OPACITY)
    text_w, text_h = shadow.size
    print(text_w, text_h)
    return shadow

def main_text_generator(txt):
    txt = txt.upper()
    main_text = TextClip(txt, font=main_font_path, fontsize=MAIN_FONT_SIZE, color='white')
    main_text = main_text.set_opacity(1)
    return main_text

def generate_subtitled_video(video_path, subtitle_data, output_path):
    video = VideoFileClip(video_path)
    
    # Create shadow subtitles
    subtitles_shadow = SubtitlesClip(subtitle_data, shadow_generator)
    # text_w, text_h = subtitles_shadow.size
    text_w = 40
    text_h = 40
    # shadow_x = (video.w - text_w) / 2 
    # shadow_y = (video.h - text_h) / 2
    shadow_x = (video.w) / 2
    shadow_y = (video.h) / 2
    subtitles_shadow = subtitles_shadow.set_position((shadow_x+10, shadow_y+10))
    # subtitles_shadow = subtitles_shadow.set_position(('center','center'))
    # subtitles_shadow = subtitles_shadow.set_position(((video.w / 2)-50 , (video.h / 2)-30 ))
    
    # Create main subtitles
    subtitles_main = SubtitlesClip(subtitle_data, main_text_generator)
    subtitles_main = subtitles_main.set_position((shadow_x, shadow_y))
    
    # Composite video with shadow and main subtitles
    result = CompositeVideoClip([video, subtitles_shadow, subtitles_main])
    
    print(f"Video dimensions: {video.w}x{video.h}")
    result.write_videofile(
        output_path,
        fps=video.fps,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        codec="libx264",
        audio_codec="aac"
    )
    
    print(f"Final video with subtitles saved to {output_path}")

# Example usage
if __name__ == '__main__':
    # Define paths
    initial_video_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/inputs/videos/video.mp4'  # Path to the original video
    final_output_path = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/main_video.mp4'

    # Load subtitle data from JSON file
    subtitles_json_path = './subs.json'
    if not os.path.exists(subtitles_json_path):
        raise FileNotFoundError(f"Subtitle JSON file not found at {subtitles_json_path}")

    with open(subtitles_json_path, 'r', encoding='utf-8') as f:
        subtitle_data = json.load(f)

    # Generate final video with both shadow and main subtitles
    generate_subtitled_video(initial_video_path, subtitle_data, final_output_path)
