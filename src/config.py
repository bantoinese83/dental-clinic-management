# src/config.py
from pathlib import Path

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv(Path(__file__).parent.parent / ".env")


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
