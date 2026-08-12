import re

from app.core.exceptions import AppError

_YOUTUBE_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?(?:.*&)?v=)([A-Za-z0-9_-]{11})"),
    re.compile(r"(?:youtu\.be/)([A-Za-z0-9_-]{11})"),
    re.compile(r"(?:youtube\.com/(?:embed|shorts)/)([A-Za-z0-9_-]{11})"),
    re.compile(r"(?:youtube\.com/v/)([A-Za-z0-9_-]{11})"),
]

_LINKEDIN_POST_RE = re.compile(r"linkedin\.com/(?:posts|feed/update)/([^/?#]+)")
_LINKEDIN_PULSE_RE = re.compile(r"linkedin\.com/pulse/[^/?#]+-([A-Za-z0-9]+)(?:/|$)")


def parse_youtube_url(url: str) -> str:
    url = url.strip()
    for pattern in _YOUTUBE_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    raise AppError(
        "Could not extract a YouTube video ID from the provided URL",
        status_code=422,
        code="invalid_youtube_url",
    )


def parse_linkedin_post_id(url: str) -> str:
    url = url.strip()
    match = _LINKEDIN_POST_RE.search(url)
    if match:
        return re.sub(r"[^A-Za-z0-9_.\-]", "_", match.group(1).replace(".html", ""))
    match = _LINKEDIN_PULSE_RE.search(url)
    if match:
        return match.group(1)
    raise AppError(
        "Could not extract a LinkedIn post ID from the provided URL",
        status_code=422,
        code="invalid_linkedin_url",
    )
