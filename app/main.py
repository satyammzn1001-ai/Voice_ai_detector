from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.auth import verify_api_key
from app.audio_utils import base64_to_audio
from app.model import predict
security = HTTPBearer()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # sab allow (development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/detect-voice")
def detect_voice(
    req: AudioRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_api_key(credentials)

    audio = base64_to_audio(req.audio_base64)
    result, confidence = predict(audio)

    return {
        "result": result,
        "confidence": confidence
    }

