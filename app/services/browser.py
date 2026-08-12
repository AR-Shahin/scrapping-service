import os
import threading

from playwright.sync_api import BrowserContext, Playwright, sync_playwright

from app.core.config import get_settings

_thread_local = threading.local()


def get_context() -> tuple[Playwright, BrowserContext]:
    cached = getattr(_thread_local, "linkedin_context", None)
    if cached is not None:
        return cached

    settings = get_settings()
    user_data_dir = os.path.expanduser(settings.linkedin_user_data_dir)
    playwright = sync_playwright().start()
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=settings.linkedin_headless,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        timeout=settings.browser_launch_timeout_ms,
    )
    _thread_local.linkedin_context = (playwright, context)
    return playwright, context
