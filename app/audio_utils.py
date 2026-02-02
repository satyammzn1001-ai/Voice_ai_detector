import base64, tempfile, librosa

def base64_to_audio(audio_base64: str):
    audio_bytes = base64.b64decode(audio_base64)

    with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
        f.write(audio_bytes)
        f.flush()
        audio, _ = librosa.load(f.name, sr=16000, mono=True)

    return audio
