# syntax=docker/dockerfile:1.7

FROM python:3.11-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /build

RUN pip install --no-cache-dir pip==25.1

COPY --link requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv \
    && /opt/venv/bin/pip install -r requirements.txt

RUN /opt/venv/bin/playwright install chromium-headless-shell

FROM python:3.11-slim-bookworm AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

COPY --from=builder --link /opt/venv /opt/venv
COPY --from=builder --link /ms-playwright /ms-playwright

RUN --mount=type=cache,target=/var/cache/apt \
    python -m playwright install-deps chromium-headless-shell \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/false appuser

COPY --link --chown=appuser:appuser app ./app

USER appuser

EXPOSE 8000

LABEL org.opencontainers.image.title="Content Extractor API" \
      org.opencontainers.image.description="YouTube and LinkedIn content extraction service" \
      org.opencontainers.image.version="1.0.0"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
