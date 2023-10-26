from semantic_ai.indexer.constants import (
    ELASTIC_SEARCH,
    QDRANT
)
from semantic_ai.indexer.elastic_search import ElasticSearchIndexer
from semantic_ai.indexer.qdrant import QdrantIndexer

__all__ = [
    "ElasticSearchIndexer",
    "QdrantIndexer"
]


def source_name_list():
    list_ = [
        ELASTIC_SEARCH,
        QDRANT
    ]
    return list_


class Indexer:

    def __init__(self, source_name: str, *args, **kwargs):
        self.source_name = source_name
        if self.source_name == ELASTIC_SEARCH:
            self.client = ElasticSearchIndexer(*args, **kwargs)
        elif self.source_name == QDRANT:
            self.client = QdrantIndexer(*args, **kwargs)
        else:
            raise ValueError(
                f"Source name is not valid. Please give the following source name and that credentials -> "
                f"{source_name_list()}"
            )

    def create(self):
        return self.client.create()
