import os

from pydantic.v1 import BaseSettings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):

    SHARE_POINT_CLIENT_ID: str = os.getenv("SHARE_POINT_CLIENT_ID", "")
    SHARE_POINT_CLIENT_SECRET: str = os.getenv("SHARE_POINT_CLIENT_SECRET", "")
    SHARE_POINT_TENANT_ID: str = os.getenv("SHARE_POINT_TENANT_ID", "")
    SHARE_POINT_HOST_NAME: str = os.getenv("SHARE_POINT_HOST_NAME", "")

    class Config:
        case_sensitive = True


settings = Settings()
