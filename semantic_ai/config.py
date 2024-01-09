import os

from pydantic import BaseModel, BaseSettings, ConfigDict


# from pydantic_settings import BaseSettings, SettingsConfigDict


class Sharepoint(BaseModel):
    # model_config = ConfigDict(env_prefix="SHAREPOINT", case_sensitive=False)
    client_id: str = os.getenv("SHAREPOINT_CLIENT_ID")
    client_secret: str = os.getenv("SHAREPOINT_CLIENT_SECRET")
    tenant_id: str = os.getenv("SHAREPOINT_TENANT_ID")
    host_name: str = os.getenv("SHAREPOINT_HOST_NAME")
    scope: str = os.getenv("SHAREPOINT_SCOPE")
    site_id: str = os.getenv("SHAREPOINT_SITE_ID")
    drive_id: str = os.getenv("SHAREPOINT_DRIVE_ID")
    folder_url: str = os.getenv("SHAREPOINT_FOLDER_URL")


class Elasticsearch(BaseModel):
    # model_config = ConfigDict(env_prefix="ELASTICSEARCH", case_sensitive=False)
    url: str = os.getenv("ELASTICSEARCH_URL")
    user: str = os.getenv("ELASTICSEARCH_USER")
    password: str = os.getenv("ELASTICSEARCH_PASSWORD")
    index_name: str = os.getenv("ELASTICSEARCH_INDEX_NAME")
    ssl_verify: bool = os.getenv("ELASTICSEARCH_SSL_VERIFY")


class Qdrant(BaseModel):
    # model_config = ConfigDict(env_prefix="QDRANT", case_sensitive=False)
    url: str = os.getenv("QDRANT_URL")
    api_key: str = os.getenv("QDRANT_INDEX_NAME")
    index_name: str = os.getenv("QDRANT_API_KEY")


class LLM(BaseModel):
    # model_config = ConfigDict(env_prefix="LLM", case_sensitive=False)
    model: str = os.getenv("LLM_MODEL")
    model_name_or_path: str = os.getenv("LLM_MODEL_NAME_OR_PATH")


class IBM(BaseModel):
    # model_config = ConfigDict(env_prefix="IBM", case_sensitive=False)
    url: str = os.getenv("IBM_URL")
    api_key: str = os.getenv("IBM_API_KEY")
    project_id: str = os.getenv("IBM_PROJECT_ID")


class Embed(BaseModel):
    # model_config = ConfigDict(env_prefix="EMBED", case_sensitive=False)
    model_name: str = os.getenv("EMBED_MODEL_NAME")


class Sqlite(BaseModel):
    # model_config = SettingsConfigDict(env_prefix="SQLITE", case_sensitive=False)
    sql_path: str = os.getenv("SQLITE_SQL_PATH")


class Mysql(BaseModel):
    # model_config = SettingsConfigDict(env_prefix="MYSQL", case_sensitive=False)
    host: str = os.getenv("MYSQL_HOST")
    user: str = os.getenv("MYSQL_USER")
    password: str = os.getenv("MYSQL_PASSWORD")
    database: str = os.getenv("MYSQL_DATABASE")
    port: str = os.getenv("MYSQL_PORT")


class Sqlserver(BaseModel):
    # model_config = SettingsConfigDict(env_prefix="MYSQL", case_sensitive=False)
    host: str = os.getenv("SQLSERVER_HOST")
    user: str = os.getenv("SQLSERVER_USER")
    password: str = os.getenv("SQLSERVER_PASSWORD")
    database: str = os.getenv("SQLSERVER_DATABASE")
    driver: str = os.getenv("SQLSERVER_DRIVER")


class Settings(BaseSettings):
    # model_config = ConfigDict(env_nested_delimiter='__', extra='ignore')
    connector_type: str
    indexer_type: str
    embedding_type: str
    file_download_dir_path: str
    extracted_dir_path: str

    embed: Embed = Embed()
    sharepoint: Sharepoint = Sharepoint()
    llm: LLM = LLM()
    elasticsearch: Elasticsearch = Elasticsearch()
    qdrant: Qdrant = Qdrant()
    ibm: IBM = IBM()
    sqlite: Sqlite = Sqlite()
    mysql: Mysql = Mysql()
    sqlserver: Sqlserver = Sqlserver()
