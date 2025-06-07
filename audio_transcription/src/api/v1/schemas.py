from pydantic import BaseModel
from typing import List, Optional

class SpeakerTurn(BaseModel):
    speaker: str
    start_time: float
    end_time: float
    transcript: str

class TranscriptionResponse(BaseModel):
    full_transcript: str
    diarization: List[SpeakerTurn]

class TitleSuggestionRequest(BaseModel):
    text: str
    count: Optional[int] = 5

class TitleSuggestionResponse(BaseModel):
    titles: List[str] 