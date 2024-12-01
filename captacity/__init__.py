import time
from moviepy.editor import VideoFileClip, CompositeVideoClip
import subprocess
import tempfile
import os

from captacity import segment_parser
from captacity import transcriber
from captacity.text_drawer import (get_text_size_ex, create_text_ex, blur_text_clip, Word)

def detect_local_whisper(print_info=False):
    """
    Detect whether the local Whisper model is available.

    Returns:
        bool: True if the local Whisper model is detected, False otherwise.
    """
    try:
        import whisper
        if print_info:
            print("Local Whisper model detected.")
        return True
    except ImportError:
        if print_info:
            print("Local Whisper model not found. Using API.")
        return False

def calculate_lines(text, font, font_size, stroke_width, text_bbox_width, max_words_per_line=None):
    """
    Splits text into lines that fit within the bounding box width.

    Args:
        text (str): The text to split into lines.
        font (str): The path to the font file.
        font_size (int): The size of the font.
        stroke_width (int): The width of the stroke.
        text_bbox_width (int): The maximum width of the bounding box.
        max_words_per_line (int): Maximum words allowed per line (optional).

    Returns:
        dict: A dictionary containing the lines of text and their total height.
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        line_width, line_height = get_text_size_ex(test_line, font, font_size, stroke_width)

        if line_width <= text_bbox_width and (max_words_per_line is None or len(current_line) + 1 <= max_words_per_line):
            current_line.append(word)
        else:
            lines.append({"text": " ".join(current_line), "width": line_width, "height": line_height})
            current_line = [word]

    # Add the last line
    if current_line:
        line_width, line_height = get_text_size_ex(" ".join(current_line), font, font_size, stroke_width)
        lines.append({"text": " ".join(current_line), "width": line_width, "height": line_height})

    # Calculate total height
    total_height = sum(line["height"] for line in lines)

    return {"lines": lines, "height": total_height}

def add_captions(
    video_file,
    output_file="with_transcript.mp4",
    font="Bangers-Regular.ttf",
    font_size=130,
    font_color="yellow",
    stroke_width=3,
    stroke_color="black",
    highlight_current_word=True,
    word_highlight_color="red",
    line_count=2,
    max_words_per_frame=None,
    padding=50,
    shadow_strength=1.0,
    shadow_blur=0.1,
    print_info=False,
    initial_prompt=None,
    segments=None,
    use_local_whisper="auto",
):
    _start_time = time.time()

    font = 'C:/Users/ryana/Documents/VsCode/VideoGenerator/VideoGenerator-main/VideoGenerator-main/subtitles/Montserrat-Black.ttf'

    if print_info:
        print("Extracting audio...")

    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav").name

    subprocess.run([
        'ffmpeg', '-y', '-i', video_file, temp_audio_file
    ], check=True)

    if segments is None:
        if print_info:
            print("Transcribing audio...")

        if use_local_whisper == "auto":
            use_local_whisper = detect_local_whisper(print_info)

        if use_local_whisper:
            segments = transcriber.transcribe_locally(temp_audio_file, initial_prompt, max_words_per_frame)
        else:
            segments = transcriber.transcribe_with_api(temp_audio_file, initial_prompt, max_words_per_frame)

    if print_info:
        print("Generating video elements...")

    video = VideoFileClip(video_file)
    text_bbox_width = video.w - padding * 2
    clips = [video]

    captions = segment_parser.parse(
        segments=segments,
        fit_function=lambda text: len(calculate_lines(
            text,
            font,
            font_size,
            stroke_width,
            text_bbox_width,
            max_words_per_line=max_words_per_frame,
        )["lines"]) <= line_count,
        max_words_per_frame=2  # Pass word limit here(Only working Input)
    )

    for caption in captions:
        line_data = calculate_lines(caption["text"], font, font_size, stroke_width, text_bbox_width, max_words_per_frame)

        text_y_offset = video.h // 2 - line_data["height"] // 2
        for line in line_data["lines"]:
            pos = ("center", text_y_offset)

            text = create_text_ex(
                [Word(w) for w in line["text"].split()],
                font_size, font_color, font, stroke_color=stroke_color, stroke_width=stroke_width
            )
            text = text.set_start(caption["start"])
            text = text.set_duration(caption["end"] - caption["start"])
            text = text.set_position(pos)
            clips.append(text)

            text_y_offset += line["height"]

    end_time = time.time()
    generation_time = end_time - _start_time

    if print_info:
        print(f"Generated in {generation_time//60:02.0f}:{generation_time%60:02.0f}")

    if print_info:
        print("Rendering video...")

    video_with_text = CompositeVideoClip(clips)

    video_with_text.write_videofile(
        filename=output_file,
        codec="libx264",
        fps=video.fps,
        logger="bar" if print_info else None,
    )

    if print_info:
        print(f"Captioning process complete!")
