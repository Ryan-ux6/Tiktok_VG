import captacity

# Run the captioning process
captacity.add_captions(
    video_file="C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/final/last.mp4",
    output_file="C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/outputs/final/something.mp4",

    font="C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/Montserrat-Black.ttf",
    font_size=60,
    font_color="white",

    stroke_width=0,
    stroke_color="black",

    shadow_strength=1.0,
    shadow_blur=0.9,

    highlight_current_word=True,
    word_highlight_color="yellow",

    line_count=2,
    max_words_per_frame=5,  # NEW: Limit the words per frame
    padding=50,
)

# Display a message when execution is complete
print("Captioning process complete! The output video has been saved.")
