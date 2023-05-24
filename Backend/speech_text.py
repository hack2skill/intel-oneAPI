import os
import azure.cognitiveservices.speech as speechsdk
from fastapi import UploadFile, APIRouter

# Create an instance of APIRouter
router = APIRouter()

speech_key = "a80a0c046ff54e0c8e750f8631f06a18"
service_region = "eastus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

def speech_to_text(audio_file):
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcript = result.text
    else:
        transcript = "Speech recognition failed: {}".format(result.reason)

    return transcript

@router.post("/api5")
async def convert_speech_to_text(file: UploadFile):
    file_path = f"audio_files/{file.filename}"
    os.makedirs("audio_files", exist_ok=True)
    with open(file_path, "wb") as audio:
        audio.write(await file.read())

    transcript = speech_to_text(file_path)

    return {"transcript": transcript}