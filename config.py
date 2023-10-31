import os

from typing import Set

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    CONNECTOR_TYPE: Set[str] = os.getenv("CONNECTOR_TYPE", '')
    SHARE_POINT_CLIENT_ID: Set[str] = os.getenv('SHARE_POINT_CLIENT_ID', '')
    SHARE_POINT_CLIENT_SECRET: Set[str] = os.getenv('SHARE_POINT_CLIENT_SECRET', '')
    SHARE_POINT_TENANT_ID: Set[str] = os.getenv('SHARE_POINT_TENANT_ID', '')
    SHARE_POINT_HOST_NAME: Set[str] = os.getenv('SHARE_POINT_HOST_NAME', '')

    class Config:
        case_sensitive = True


settings = Settings()
