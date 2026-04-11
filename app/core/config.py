from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: str = "8000"
    APP_DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    ALLOWED_IPS: str

    class Config:
        env_file = ".env"

settings = Settings()
ALLOWED_IPS = set(settings.ALLOWED_IPS.split(","))