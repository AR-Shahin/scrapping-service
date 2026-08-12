from typing import Any
from urllib.parse import quote

import httpx
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.exceptions import IpBlocked, NoTranscriptFound, RequestBlocked

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.utils.validators import parse_youtube_url


def extract_video_id(url: str) -> str:
    return parse_youtube_url(url)


def fetch_video_metadata(video_id: str) -> dict[str, str | None]:
    oembed_url = (
        f"https://www.youtube.com/oembed?url="
        f"{quote(f'https://www.youtube.com/watch?v={video_id}', safe='')}&format=json"
    )
    try:
        with httpx.Client(follow_redirects=True, timeout=15) as client:
            response = client.get(oembed_url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AppError(
            f"Failed to fetch metadata for video {video_id}: {exc}",
            status_code=502,
            code="youtube_fetch_error",
        ) from exc

    title = response.json().get("title")
    return {"video_id": video_id, "title": title}


def fetch_transcript(
    video_id: str,
    languages: list[str] | None = None,
) -> list[dict[str, Any]]:
    preferred = languages or get_settings().youtube_default_languages
    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=preferred)
    except (IpBlocked, RequestBlocked) as exc:
        raise AppError(
            f"YouTube is blocking requests for video {video_id} from this IP. "
            "This is common for cloud/datacenter IPs.",
            status_code=403,
            code="youtube_ip_blocked",
        ) from exc
    except NoTranscriptFound as exc:
        raise AppError(
            f"No transcript found for video {video_id} in the requested languages.",
            status_code=404,
            code="transcript_not_found",
        ) from exc
    except Exception as exc:
        raise AppError(
            f"Could not fetch a transcript for video {video_id}: {exc}",
            status_code=404,
            code="transcript_not_found",
        ) from exc

    return [
        {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
        for snippet in fetched
    ]


def extract_video(url: str, languages: list[str] | None = None) -> dict[str, Any]:
    video_id = extract_video_id(url)
    metadata = fetch_video_metadata(video_id)
    segments = fetch_transcript(video_id, languages)
    full_transcript = " ".join(segment["text"] for segment in segments)
    return {
        "video_id": video_id,
        "title": metadata["title"],
        "full_transcript": full_transcript,
        "segments": segments,
    }
