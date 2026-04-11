import pkgutil, importlib
from fastapi import FastAPI, Request
from app.core.security import check_ip
from app.core.config import settings
import uvicorn

app = FastAPI()

@app.middleware("http")
async def middleware(request: Request, call_next):
    check_ip(request)
    return await call_next(request)

for _, name, _ in pkgutil.iter_modules(["app/modules"]):
    module = importlib.import_module(f"app.modules.{name}.router")
    app.include_router(module.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=str(settings.APP_HOST),
        port=int(settings.APP_PORT),
        log_level='trace' if not settings.APP_DEBUG else 'debug',
        reload=True,
        factory=True,
    )