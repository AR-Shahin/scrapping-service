from fastapi import APIRouter

from app.schemas.linkedin import LinkedInExtractRequest, LinkedInExtractResponse
from app.services import linkedin as linkedin_service

router = APIRouter()


@router.post(
    "/linkedin",
    response_model=LinkedInExtractResponse,
    summary="Extract LinkedIn post content",
)
def extract_linkedin(payload: LinkedInExtractRequest) -> LinkedInExtractResponse:
    return linkedin_service.scrape_post(str(payload.url))
