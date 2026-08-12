from pydantic import BaseModel, Field, HttpUrl


class YouTubeExtractRequest(BaseModel):
    url: HttpUrl
    languages: list[str] | None = Field(
        default=None,
        description="Preferred transcript languages in priority order. "
        "Defaults to the service-configured list.",
    )


class YouTubeTranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float


class YouTubeExtractResponse(BaseModel):
    video_id: str
    title: str | None = None
    full_transcript: str
    segments: list[YouTubeTranscriptSegment]
