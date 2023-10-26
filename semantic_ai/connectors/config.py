import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    SHARE_POINT_CLIENT_ID: str = os.getenv("SHARE_POINT_CLIENT_ID", "")
    SHARE_POINT_CLIENT_SECRET: str = os.getenv("SHARE_POINT_CLIENT_SECRET", "")
    SHARE_POINT_TENANT_ID: str = os.getenv("SHARE_POINT_TENANT_ID", "")
    SHARE_POINT_HOST_NAME: str = os.getenv("SHARE_POINT_HOST_NAME", "")

    class Config:
        case_sensitive = True


settings = Settings()
