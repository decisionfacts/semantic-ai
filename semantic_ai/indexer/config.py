import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    ELASTIC_SEARCH_URL: str = os.getenv("ELASTIC_SEARCH_URL", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", None)

    class Config:
        case_sensitive = True


settings = Settings()
