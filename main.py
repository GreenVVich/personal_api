import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level="trace" if not settings.APP_DEBUG else "debug",
        reload=True,
        factory=True,
    )
