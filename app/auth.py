from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.config import API_KEY

def verify_api_key(credentials: HTTPAuthorizationCredentials):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
