from fastapi import FastAPI
from src.api.v1.endpoints import transcription

app = FastAPI(title="AI Transcription & Content Service")

# Include API v1 routers
app.include_router(transcription.router, prefix="/api/v1", tags=["Transcription"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the AI Service!"} 