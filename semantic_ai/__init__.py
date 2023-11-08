import logging
from semantic_ai.connectors import get_connectors
from semantic_ai.indexer import get_indexer
from semantic_ai.llm import get_llm
from semantic_ai.config import Sharepoint, Elasticsearch, Settings, LLM, Qdrant
from semantic_ai.utils import iter_to_aiter, make_dirs, generate_llama_simple_prompt_template
from semantic_ai.extract import extract as df_extract
from semantic_ai import constants
from semantic_ai.search.semantic_search import Search

from langchain.embeddings.openai import OpenAIEmbeddings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def _load_settings(settings: Settings | None = None):
    if not settings:
        settings = Settings()
        return settings
    else:
        return settings


async def __embed_obj(_type, model_name):
    if _type == "openai":
        embeddings = OpenAIEmbeddings(model=model_name) if model_name else OpenAIEmbeddings()
        return embeddings


async def __index_obj_create(settings: Settings | None = None):
    settings = await _load_settings(settings)
    if settings.indexer_type == constants.ELASTIC_SEARCH:
        elastic_search: Elasticsearch = settings.elasticsearch
        if not settings.embedding_type:
            index_obj = await get_indexer(
                settings.indexer_type,
                url=elastic_search.url,
                es_user=elastic_search.user,
                es_password=elastic_search.password,
                index_name=elastic_search.index_name,
                ssl_verify=elastic_search.ssl_verify
            )
        else:
            _embed = await __embed_obj(settings.embedding_type, settings.embed.model_name)
            index_obj = await get_indexer(
                settings.indexer_type,
                url=elastic_search.url,
                es_user=elastic_search.user,
                es_password=elastic_search.password,
                index_name=elastic_search.index_name,
                ssl_verify=elastic_search.ssl_verify,
                embedding=_embed
            )
    elif settings.indexer_type == constants.QDRANT:
        qdrant: Qdrant = settings.qdrant
        if not settings.embedding_type:
            index_obj = await get_indexer(
                settings.indexer_type,
                url=qdrant.url,
                api_key=qdrant.api_key,
                index_name=qdrant.index_name
            )
        else:
            _embed = await __embed_obj(settings.embedding_type, settings.embed.model_name)
            index_obj = await get_indexer(
                settings.indexer_type,
                url=qdrant.url,
                api_key=qdrant.api_key,
                index_name=qdrant.index_name,
                embedding=_embed
            )
    return index_obj


async def download(settings: Settings | None = None):
    settings = await _load_settings(settings)
    logger.info(f"Initiated download process")
    if settings.connector_type:
        if settings.connector_type == constants.SHARE_POINT:
            sharepoint: Sharepoint = settings.sharepoint
            try:
                _download = await get_connectors(settings.connector_type,
                                                 client_id=sharepoint.client_id,
                                                 client_secret=sharepoint.client_secret,
                                                 tenant_id=sharepoint.tenant_id,
                                                 host_name=sharepoint.host_name,
                                                 scope=sharepoint.scope
                                                 )
                logger.info(f"{sharepoint.type.capitalize()} object created")
                await _download.download(site_id=sharepoint.site_id,
                                         drive_id=sharepoint.drive_id,
                                         folder_url=sharepoint.folder_url)
            except Exception as ex:
                logger.info(f"Download failed")
                logger.error(ex)
    else:
        raise ValueError(f"Give valid credentials or load properly environment variable.")


async def extract(settings: Settings | None = None):
    settings = await _load_settings(settings)

    downloaded_path = None
    extracted_output_dir = ""
    logger.info(f"Extraction initiated")
    downloaded_path = settings.file_download_dir_path
    extracted_output_dir = settings.extracted_dir_path
    downloaded_path = await make_dirs(downloaded_path, constants.DEFAULT_FOLDER_NAME)
    extracted_output_dir = await make_dirs(extracted_output_dir, constants.JSON_OUTPUT_DIR)
    await df_extract(file_path=downloaded_path,
                     output_dir=extracted_output_dir,
                     as_json=True)


async def index(settings: Settings | None = None):
    settings = await _load_settings(settings)

    logger.info(f"Index starting")
    extracted_output_dir = ""
    if settings.indexer_type:
        extracted_output_dir = settings.extracted_dir_path
        extracted_output_dir = await make_dirs(extracted_output_dir, constants.JSON_OUTPUT_DIR)
        try:
            index_obj = await __index_obj_create()
            await index_obj.index(extracted_output_dir)
            logger.info(f"{settings.indexer_type.capitalize()} object created")
        except Exception as ex:
            logger.info("Index failed")
            logger.error(ex)
    else:
        raise ValueError(f"Give valid credentials or load properly environment variable.")


async def search(settings: Settings | None = None) -> Search:
    settings = await _load_settings(settings)
    _llm = settings.llm
    print("LLM Model", _llm.model)
    llm_obj = None
    prompt_template = None
    if _llm.model == constants.Llama:
        llm_: LLM = _llm
        llm_obj = await get_llm(_llm.model,
                                model_name_or_path=llm_.model_name_or_path
                                )
        prompt_template = await generate_llama_simple_prompt_template(constants.DEFAULT_PROMPT)
    elif _llm.model == constants.OPENAI:
        llm_: LLM = _llm
        llm_obj = await get_llm(_llm.model,
                                model_name_or_path=llm_.model_name_or_path
                                )
        prompt_template = constants.DEFAULT_PROMPT
    if not llm_obj:
        raise ValueError(f"{_llm.model} is not valid. Give valid credentials")
    llm_model = await llm_obj.llm_model()
    index_object = await __index_obj_create()
    vector_db = await index_object.create()
    return Search(model=llm_model,
                  load_vector_db=vector_db,
                  top_k=5,
                  prompt_template=prompt_template)
