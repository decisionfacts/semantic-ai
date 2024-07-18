import os
import sys

import pytest

sys.path.extend([os.path.dirname(os.path.dirname(__file__))])

from semantic_ai.indexer import ElasticsearchIndexer

user = "sssss"
password = "password"
url = "http://localhost:9200/"

elasticsearch_obj = ElasticsearchIndexer(
    user=user,
    password=password,
    url=url,
    index_name="<index_name>"
)


# Have to mention file path or directory path
@pytest.mark.asyncio
async def test_index():
    await elasticsearch_obj.index("<file_path>")


# have to mention index name
@pytest.mark.asyncio
async def test_delete_index():
    await elasticsearch_obj.delete("<index_name>")
