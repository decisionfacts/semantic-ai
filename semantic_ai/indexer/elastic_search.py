from typing import (
    Any,
    Dict,
    Optional
)
from semantic_ai.embeddings.base import BaseEmbeddings
from langchain.vectorstores import ElasticVectorSearch


class ElasticSearchIndexer:

    def __init__(
            self,
            elasticsearch_url: str,
            index_name: str,
            embedding: BaseEmbeddings,
            ssl_verify: Optional[Dict[str, Any]] = None
    ):
        self.client = ElasticVectorSearch(
            embedding=embedding,
            elasticsearch_url=elasticsearch_url,
            index_name=f"{index_name}",
            ssl_verify=ssl_verify
        )

    def create(self):
        return self.client
