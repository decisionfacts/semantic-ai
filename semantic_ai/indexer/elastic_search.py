from typing import (
    Any,
    Dict,
    Optional
)
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from semantic_ai.indexer.base import BaseIndexer
from semantic_ai.indexer.config import settings


class ElasticSearchIndexer(BaseIndexer):

    def __init__(
            self,
            index_name: str,
            url: str = settings.ELASTIC_SEARCH_URL,
            embedding: Optional[Embeddings] = HuggingFaceEmbeddings(),
            ssl_verify: Optional[Dict[str, Any]] = None
    ):
        super().__init__()
        self.client = ElasticVectorSearch(
            embedding=embedding,
            elasticsearch_url=url,
            index_name=f"{index_name}",
            ssl_verify=ssl_verify
        )

    def create(self):
        return self.client
