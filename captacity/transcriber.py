import openai
from openai._types import FileTypes

def transcribe_with_api(
    audio_file: FileTypes,
    prompt: str | None = None,
    max_words_per_frame: int | None = None
):
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_file, "rb"),
        response_format="verbose_json",
        timestamp_granularities=["segment", "word"],
        prompt=prompt
    )

    if max_words_per_frame is not None:
        transcript = _limit_words_per_frame(transcript, max_words_per_frame)

    return [{
        "start": transcript.segments[0]["start"],
        "end": transcript.segments[-1]["end"],
        "words": transcript.words,
    }]

def transcribe_locally(
    audio_file: str,
    prompt: str | None = None,
    max_words_per_frame: int | None = None
):
    import whisper

    model = whisper.load_model("base")

    transcription = model.transcribe(
        audio=audio_file,
        word_timestamps=True,
        fp16=False,
        initial_prompt=prompt,
    )

    if max_words_per_frame is not None:
        transcription = _limit_words_per_frame(transcription, max_words_per_frame)

    return transcription["segments"]

def _limit_words_per_frame(transcription, max_words_per_frame):
    limited_segments = []
    for segment in transcription.segments:
        words = segment["words"]
        for i in range(0, len(words), max_words_per_frame):
            chunk = words[i:i + max_words_per_frame]
            limited_segments.append({
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"],
                "words": chunk,
            })
    transcription["segments"] = limited_segments
    return transcription
