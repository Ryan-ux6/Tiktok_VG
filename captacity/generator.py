import captacity
import os

CURRENT_DIR = os.getcwd()
INP_FILE_NAME = "something.mp4"
OUT_FILE_NAME = "output.mp4"
FONT = "Montserrat-ExtraBold.ttf"
# Tiktok_VG\captacity\assets\fonts\Montserrat-ExtraBold.ttf
print(os.path.join(CURRENT_DIR, f"assets/content/input/video/{INP_FILE_NAME}"))

# Run the captioning process
captacity.add_captions(
    
    video_file = os.path.join(CURRENT_DIR, f"assets/content/input/video/{INP_FILE_NAME}"), # "C:/Users/HP/Desktop/2024/Extra/VideoGenerator/Ryan/Tiktok_VG/captacity/assets/content/input/video/something.mp4",
    output_file = os.path.join(CURRENT_DIR, f"assets/content/output/{OUT_FILE_NAME}"),

    font="C:/Users/HP/Desktop/2024/Extra/VideoGenerator/Ryan/Tiktok_VG/captacity/assets/fonts/Montserrat-ExtraBold.ttf", # os.path.join(CURRENT_DIR, f"assets/fonts/{FONT}"),
    font_size=60,
    font_color="white",

    stroke_width=0,
    stroke_color="black",

    shadow_strength=1.0,
    shadow_blur=0.9,

    highlight_current_word=True,
    word_highlight_color="yellow",

    line_count=1,
    padding=50,
)

# Display a message when execution is complete
print("Captioning process complete! The output video has been saved.")
