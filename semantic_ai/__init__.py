import logging
from semantic_ai.connectors import get_connectors
from semantic_ai.indexer import get_indexer
from semantic_ai.config import settings as default_settings, Sharepoint, Elasticsearch, Settings
from semantic_ai.utils import iter_to_aiter, make_dirs
from semantic_ai.extract import extract as df_extract
from semantic_ai.constants import (
    ELASTIC_SEARCH,
    SHARE_POINT,
    DEFAULT_FOLDER_NAME,
    JSON_OUTPUT_DIR
)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def _load_settings(settings: Settings | None = None):
    if not settings:
        settings = default_settings
        return settings


async def download(settings: Settings | None = None):
    settings = await _load_settings(settings)

    logger.info(f"Initiated download process")
    async for connector in iter_to_aiter(settings.connectors):
        if connector.connector_type:
            if connector.connector_type == SHARE_POINT:
                sharepoint: Sharepoint = connector
                _download = await get_connectors(sharepoint.connector_type,
                                                 client_id=sharepoint.client_id,
                                                 client_secret=sharepoint.client_secret,
                                                 tenant_id=sharepoint.tenant_id,
                                                 host_name=sharepoint.host_name,
                                                 scope=sharepoint.scope
                                                 )
                logger.info(f"{sharepoint.connector_type.capitalize()} object created")
                await _download.download(site_id=sharepoint.site_id,
                                         drive_id=sharepoint.drive_id,
                                         folder_url=sharepoint.folder_url)
        else:
            raise ValueError(f"Give valid credentials or load properly environment variable.")


async def extract(settings: Settings | None = None):
    settings = await _load_settings(settings)

    downloaded_path = None
    extracted_output_dir = ""
    logger.info(f"Extraction initiated")
    async for path in iter_to_aiter(settings.connectors):
        downloaded_path = path.file_download_dir_path
        extracted_output_dir = path.extracted_dir_path
        downloaded_path = await make_dirs(downloaded_path, DEFAULT_FOLDER_NAME)
        extracted_output_dir = await make_dirs(extracted_output_dir, JSON_OUTPUT_DIR)
    await df_extract(file_path=downloaded_path,
                     output_dir=extracted_output_dir,
                     as_json=True)


async def index(settings: Settings | None = None):
    settings = await _load_settings(settings)

    logger.info(f"Index starting")
    extracted_output_dir = ""
    async for _indexer in iter_to_aiter(settings.indexer):
        if _indexer.indexer_type:
            extracted_output_dir = _indexer.extracted_dir_path
            extracted_output_dir = await make_dirs(extracted_output_dir, JSON_OUTPUT_DIR)
            if _indexer.indexer_type == ELASTIC_SEARCH:
                elastic_search: Elasticsearch = _indexer
                index_obj = await get_indexer(elastic_search.indexer_type,
                                              url=elastic_search.url,
                                              index_name=elastic_search.index_name,
                                              ssl_verify=elastic_search.ssl_verify)
                logger.info(f"{elastic_search.indexer_type.capitalize()} object created")
                await index_obj.index(extracted_output_dir)
                logger.info(f"Index completed")
        else:
            raise ValueError(f"Give valid credentials or load properly environment variable.")
