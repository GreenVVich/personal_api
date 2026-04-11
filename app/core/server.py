import pkgutil, importlib
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from app.configuration.middlewares import __middlewares__
# from app.configuration.routes import __routes__


class Server:
    __app: FastAPI

    def __init__(self):
        self.__app = FastAPI()
        self.__register_routes()
        # self.__register_middlewares(self.__app)
        self.__app.add_middleware(  # Check for release
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app(self) -> FastAPI:
        return self.__app

    def __register_routes(self) -> None:
        for _, name, _ in pkgutil.iter_modules(["app/modules"]):
            module = importlib.import_module(f"app.modules.{name}.router")
            self.__app.include_router(module.router)

    # @staticmethod
    # def __register_middlewares(app):
    #     __middlewares__.register_middlewares(app)
