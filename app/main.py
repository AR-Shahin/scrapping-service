import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["hello"], summary="Hello")
    def hello() -> dict[str, str]:
        return {"message": f"Hello from {settings.app_name}"}

    @app.get("/health", tags=["health"], summary="Health check")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": settings.app_version}

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "code": exc.code},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "code": "internal_error"},
        )

    return app


app = create_app()
