from fastapi import FastAPI

app = FastAPI(title="AI Transcription & Content Service")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the AI Service!"} 