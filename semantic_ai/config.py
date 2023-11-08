from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Sharepoint(BaseModel):
    model_config = SettingsConfigDict(env_prefix="SHAREPOINT", case_sensitive=False)
    client_id: str
    client_secret: str
    tenant_id: str
    host_name: str
    scope: str
    site_id: str
    drive_id: str
    folder_url: str


class Elasticsearch(BaseModel):
    model_config = SettingsConfigDict(env_prefix="ELASTICSEARCH", case_sensitive=False)
    url: str
    user: str
    password: str
    index_name: str
    ssl_verify: bool


class Qdrant(BaseModel):
    model_config = SettingsConfigDict(env_prefix="QDRANT", case_sensitive=False)
    url: str
    api_key: str
    index_name: str


class LLM(BaseModel):
    model_config = SettingsConfigDict(env_prefix="LLM", case_sensitive=False)
    model: str
    model_name_or_path: str


class Embed(BaseModel):
    model_config = SettingsConfigDict(env_prefix="EMBED", case_sensitive=False)
    model_name: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__', extra='ignore')
    connector_type: str
    indexer_type: str
    embedding_type: str
    file_download_dir_path: str
    extracted_dir_path: str

    embed: Embed
    sharepoint: Sharepoint
    llm: LLM
    elasticsearch: Elasticsearch
    qdrant: Qdrant
