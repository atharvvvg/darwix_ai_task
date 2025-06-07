from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.api.v1.schemas import TranscriptionResponse
from src.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def create_transcription(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an audio file."
        )

    audio_bytes = await file.read()

    # Call the stubbed service
    result = await gemini_service.transcribe_audio_with_diarization(
        audio_file_bytes=audio_bytes,
        mime_type=file.content_type
    )
    return result 