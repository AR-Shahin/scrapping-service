from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str
    code: str = Field(default="app_error")
