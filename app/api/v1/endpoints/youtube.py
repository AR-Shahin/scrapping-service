from fastapi import APIRouter

from app.schemas.youtube import YouTubeExtractRequest, YouTubeExtractResponse
from app.services import youtube as youtube_service

router = APIRouter()


@router.post(
    "/youtube",
    response_model=YouTubeExtractResponse,
    summary="Extract YouTube video transcript",
)
def extract_youtube(payload: YouTubeExtractRequest) -> YouTubeExtractResponse:
    return youtube_service.extract_video(str(payload.url), payload.languages)
