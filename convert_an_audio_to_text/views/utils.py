import whisper
from pathlib import Path


def convert_audio(filename, model='base'):
    speech_model = whisper.load_model(model)
    result = speech_model.transcribe(f'media/{filename}', fp16=False)
    return result['text']


def check_extention(filename):
    ext = Path(filename).suffix
    if not (ext.lower() in ['.mp3', '.wav']):
        return False
    else:
        return True