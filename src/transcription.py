# import os
# from huggingface_hub import InferenceClient
# from dotenv import load_dotenv



# load_dotenv()          # this code is for higging face

  

# client = InferenceClient(
#     api_key=os.getenv("HUGGINGFACE_API_KEY")
# )

# def transcribe_audio(audio_path):
#     """
#     Transcribe audio using Hugging Face Whisper Api.
#     """
    
#     with open(audio_path, "rb") as audio_file:
#         audio_bytes = audio_file.read()

#     result = client.automatic_speech_recognition(
#         audio_bytes,
#         model="openai/whisper-large-v3",
#     )
        
#     if isinstance(result, dict):
#         return result.get("text","")

#     if hasattr(result, "text"):
#         return result.text
    
#     return str(result)


#--------------------------------------------------------

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
    """

    with open(audio_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            temperature=0.0,
            response_format = "verbose_json"
        )

    return transcription.text