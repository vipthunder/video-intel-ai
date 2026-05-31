import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def transcribe_audio(audio_path):
    """
    Transcribe audio using Groq Whisper API.
    Returns:
        [
            {
                "text": "...",
                "start": 0.0,
                "end": 5.2
            }
        ]
    """

    with open(audio_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            temperature=0.0,
            response_format="verbose_json"
        )

    segments = []

    for segment in transcription.segments:

        text = segment["text"].strip()

        if not text:
            continue

        segments.append(
            {
                "text": text,
                "start": float(segment["start"]),
                "end": float(segment["end"])
            }
        )

    return segments
