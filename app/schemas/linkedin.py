from pydantic import BaseModel, Field, HttpUrl


class LinkedInExtractRequest(BaseModel):
    url: HttpUrl


class LinkedInExtractResponse(BaseModel):
    post_id: str
    url: str
    author: str | None = None
    text: str
    comments: list[str] = Field(default_factory=list)
