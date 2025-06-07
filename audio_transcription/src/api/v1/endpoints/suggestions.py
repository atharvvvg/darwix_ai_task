from fastapi import APIRouter
from src.api.v1.schemas import TitleSuggestionRequest, TitleSuggestionResponse
from src.services.gemini_service import gemini_service

router = APIRouter()

@router.post("/suggest-titles", response_model=TitleSuggestionResponse)
async def create_title_suggestions(request: TitleSuggestionRequest):
    # Call the stubbed service
    titles = await gemini_service.generate_title_suggestions(
        text=request.text,
        count=request.count
    )
    return {"titles": titles} 