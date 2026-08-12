import pytest

from app.core.exceptions import AppError
from app.utils.validators import parse_linkedin_post_id, parse_youtube_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=abcDEFghIJK&t=42", "abcDEFghIJK"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ],
)
def test_parse_youtube_url(url: str, expected: str) -> None:
    assert parse_youtube_url(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=tooshort",
        "",
    ],
)
def test_parse_youtube_url_invalid(url: str) -> None:
    with pytest.raises(AppError):
        parse_youtube_url(url)


@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://www.linkedin.com/posts/john-doe_abc-123-456/",
            "john-doe_abc-123-456",
        ),
        (
            "https://www.linkedin.com/feed/update/urn:li:activity:7123456789012345678/",
            "urn_li_activity_7123456789012345678",
        ),
        (
            "https://www.linkedin.com/pulse/7-type-database-khalid-hasan-i2cxc/",
            "i2cxc",
        ),
    ],
)
def test_parse_linkedin_post_id(url: str, expected: str) -> None:
    assert parse_linkedin_post_id(url) == expected


@pytest.mark.parametrize(
    "url",
    ["https://example.com/posts/abc", "https://www.linkedin.com/feed/", ""],
)
def test_parse_linkedin_post_id_invalid(url: str) -> None:
    with pytest.raises(AppError):
        parse_linkedin_post_id(url)
