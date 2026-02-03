from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import os

from app.auth import verify_api_key
from app.model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-voice")
def detect_voice(
    audio: UploadFile = File(...),      # 🔴 MP3 file
    _: bool = Depends(verify_api_key)   # x-api-key auth
):
    # Save uploaded MP3 temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio.file, tmp)
        audio_path = tmp.name

    # Predict
    result, confidence, explanation = predict(audio_path)

    # Cleanup
    os.remove(audio_path)

    return {
        "result": result,
        "confidence": float(confidence),
        "explanation": explanation
    }
