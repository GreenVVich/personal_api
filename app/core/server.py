import importlib
import pkgutil
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.logging import get_logger

# from app.configuration.middlewares import __middlewares__
# from app.configuration.routes import __routes__


logger = get_logger("server")


class Server:
    __app: FastAPI

    def __init__(self) -> None:
        self.__app = FastAPI(lifespan=self.__lifespan)
        self.__register_routes()
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app(self) -> FastAPI:
        return self.__app

    @asynccontextmanager
    async def __lifespan(self, _app: FastAPI):
        logger.info("Application startup")
        try:
            yield
        finally:
            logger.info("Application shutdown")

    def __register_routes(self) -> None:
        for _, name, _ in pkgutil.iter_modules(["app/modules"]):
            module = importlib.import_module(f"app.modules.{name}.router")
            self.__app.include_router(module.router)
