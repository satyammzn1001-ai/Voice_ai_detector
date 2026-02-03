from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.auth import verify_api_key
from app.audio_utils import base64_to_audio
from app.model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # 🔴 IMPORTANT
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/detect-voice")
def detect_voice(
    req: AudioRequest,
    _: bool = Depends(verify_api_key)   # x-api-key auth
):
    audio = base64_to_audio(req.audio_base64)
    result, confidence = predict(audio)

    return {
        "result": result,
        "confidence": float(confidence)
    }
