from typing import Callable

def has_partial_sentence(text):
    words = text.split()
    if len(words) >= 2:
        prev_word = text.split()[-2].strip()
        if prev_word[-1] == ".":
            return True
    return False

def parse(
    segments: list[dict],
    fit_function: Callable,
    allow_partial_sentences: bool = False,
    max_words_per_frame: int = 2,  # Ensure parameter is forwarded
):
    captions = []
    caption = {
        "start": None,
        "end": 0,
        "words": [],
        "text": "",
    }

    for segment in segments:
        for word in segment["words"]:
            if caption["start"] is None:
                caption["start"] = word["start"]

            text = caption["text"] + word["word"]

            caption_fits = (
                allow_partial_sentences or not has_partial_sentence(text)
            ) and fit_function(text)

            if max_words_per_frame and len(caption["words"]) >= max_words_per_frame:
                caption_fits = False

            if caption_fits:
                caption["words"].append(word)
                caption["end"] = word["end"]
                caption["text"] = text
            else:
                captions.append(caption)
                caption = {
                    "start": word["start"],
                    "end": word["end"],
                    "words": [word],
                    "text": word["word"],
                }

    if caption["words"]:
        captions.append(caption)

    return captions
