import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    debug: bool = os.environ.get("DEBUG", "")

    FASTAPI_CONFIG: str = os.getenv("FASTAPI_CONFIG", "")
    GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID", "")
    ACCESS_KEY: str = os.environ.get("ACCESS_KEY", "")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    STATIC_FILE: str = "static"
    SENTRY_DSN: str = os.environ.get("SENTRY_DSN", "")
    PAGINATION_SIZE: int = os.environ.get("PAGINATION_SIZE", 50)

    ADMIN_AUTH_KEY: str = os.environ.get("ADMIN_AUTH_KEY", "")

settings = Settings()
