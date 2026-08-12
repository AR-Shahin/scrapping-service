from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Content Extractor API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    linkedin_email: str | None = None
    linkedin_password: str | None = None
    linkedin_user_data_dir: str = "~/.linkedin_browser_profile"
    linkedin_headless: bool = True
    browser_launch_timeout_ms: int = 60000
    browser_navigation_timeout_ms: int = 60000

    youtube_default_languages: list[str] = ["en", "bn", "hi"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
