from typing import (
    Any,
    Dict,
    Optional
)
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from semantic_ai.indexer.base import BaseIndexer


class ElasticSearchIndexer(BaseIndexer):

    def __init__(
            self,
            url: str,
            index_name: str,
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

    async def create(self):
        return self.client
