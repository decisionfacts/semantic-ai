import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from distutils.util import strtobool


class Connector(BaseModel):
    connector_type: str = os.getenv("CONNECTOR_TYPE", None)
    file_download_dir_path: str = os.getenv("FILE_DOWNLOAD_DIR_PATH", None)
    extracted_dir_path: str = os.getenv("EXTRACTED_DIR_PATH", None)


class Indexer(BaseModel):
    indexer_type: str = os.getenv("INDEXER_TYPE", None)
    extracted_dir_path: str = os.getenv("EXTRACTED_DIR_PATH", None)


class Sharepoint(Connector):
    client_id: str = os.getenv('SHAREPOINT_CLIENT_ID')
    client_secret: str = os.getenv('SHAREPOINT_CLIENT_SECRET')
    tenant_id: str = os.getenv('SHAREPOINT_TENANT_ID')
    host_name: str = os.getenv('SHAREPOINT_HOST_NAME')
    scope: str = os.getenv("SHAREPOINT_SCOPE")
    site_id: str = os.getenv('SHAREPOINT_SITE_ID')
    drive_id: str = os.getenv('SHAREPOINT_DRIVE_ID')
    folder_url: str = os.getenv('SHAREPOINT_FOLDER_URL')


class Elasticsearch(Indexer):
    url: str = os.getenv('ELASTICSEARCH_URL', '')
    index_name: str = os.getenv('ELASTICSEARCH_INDEX_NAME', '')
    ssl_verify: bool = strtobool(os.getenv('ELASTICSEARCH_SSL_VERIFY', 'True'))


class Settings(BaseSettings):
    connectors: list[Sharepoint] = [Sharepoint()]
    indexer: list[Elasticsearch] = [Elasticsearch()]
    #
    # class Config:
    #     case_sensitive = True


settings = Settings()
