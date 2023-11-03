from semantic_ai.indexer.elastic_search import ElasticsearchIndexer
from semantic_ai.indexer.qdrant import QdrantIndexer

from semantic_ai.utils import get_dynamic_class
from semantic_ai.constants import INDEXER_LIST

__all__ = [
    "ElasticsearchIndexer",
    "QdrantIndexer",
    "get_indexer"
]


async def get_indexer(index_type: str, **kwargs):
    if index_type not in INDEXER_LIST:
        raise ValueError(f"Please give the below following index type.{INDEXER_LIST}")
    indexer_cls = await get_dynamic_class(
        class_name=f"{index_type.capitalize()}Indexer",
        module_name=f"semantic_ai.indexer"
    )
    return indexer_cls(**kwargs)
