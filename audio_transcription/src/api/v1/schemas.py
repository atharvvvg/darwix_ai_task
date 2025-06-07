from pydantic import BaseModel
from typing import List

class SpeakerTurn(BaseModel):
    speaker: str
    start_time: float
    end_time: float
    transcript: str

class TranscriptionResponse(BaseModel):
    full_transcript: str
    diarization: List[SpeakerTurn] 