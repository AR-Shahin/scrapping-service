import logging
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.services.browser import get_context
from app.utils.validators import parse_linkedin_post_id

logger = logging.getLogger(__name__)

_AUTHOR_SELECTORS = [
    ".feed-shared-actor__title",
    ".update-components-actor__name",
]

_TEXT_SELECTORS = [
    ".feed-shared-inline-feed-story__text",
    ".feed-shared-text__visible-text-box",
    '[data-test-id="main-feed-activity-card__commentary"]',
    ".feed-shared-update-v2__commentary",
    ".show-more-less-html__markup",
    ".article-content",
    "article",
]

_COMMENT_SELECTORS = [
    ".comments-comment-item-content-body",
    ".comment__content",
]


def _first_text(page, selectors: list[str]) -> str:
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.count() > 0:
            text = locator.inner_text()
            if text and text.strip():
                return text.strip()
    return ""


def _all_texts(page, selectors: list[str]) -> list[str]:
    for selector in selectors:
        locator = page.locator(selector)
        texts = [
            element.inner_text().strip()
            for element in locator.all()
            if element.inner_text().strip()
        ]
        if texts:
            return texts
    return []


def _meta_description(page) -> str:
    meta = page.locator('meta[property="og:description"]').first
    if meta.count() > 0:
        content = meta.get_attribute("content")
        if content:
            return content.strip()
    return ""


def _handle_authwall(page) -> None:
    settings = get_settings()
    if "authwall" in page.url or page.locator(".authwall-join-form").count() > 0:
        email = settings.linkedin_email
        password = settings.linkedin_password
        if not email or not password:
            raise AppError(
                "LinkedIn login wall detected. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD "
                "in .env (first login may require manual verification).",
                status_code=403,
                code="linkedin_login_required",
            )
        page.locator("input#session_key").fill(email)
        page.locator("input#session_password").fill(password)
        page.locator("input#session_password").press("Enter")
        page.wait_for_timeout(6000)


def _expand_content(page) -> None:
    expand = page.locator("button.show-more-less-html__button--more").first
    if expand.count() > 0:
        expand.click()
        page.wait_for_timeout(1500)


def scrape_post(url: str) -> dict[str, Any]:
    post_id = parse_linkedin_post_id(url)
    settings = get_settings()
    _, context = get_context()
    page = context.new_page()

    try:
        nav = {"wait_until": "domcontentloaded", "timeout": settings.browser_navigation_timeout_ms}
        page.goto(url, **nav)
        page.wait_for_timeout(4000)
        _handle_authwall(page)
        if "authwall" in page.url:
            page.goto(url, **nav)
            page.wait_for_timeout(4000)
        _expand_content(page)

        author = _first_text(page, _AUTHOR_SELECTORS)
        post_text = _first_text(page, _TEXT_SELECTORS)
        comments = _all_texts(page, _COMMENT_SELECTORS)
        if not post_text:
            post_text = _meta_description(page)
        final_url = page.url
    finally:
        page.close()

    if not post_text:
        raise AppError(
            "Could not extract post content. The page may require login or "
            "LinkedIn changed its layout.",
            status_code=404,
            code="linkedin_content_not_found",
        )

    return {
        "post_id": post_id,
        "url": final_url,
        "author": author,
        "text": post_text,
        "comments": comments,
    }
