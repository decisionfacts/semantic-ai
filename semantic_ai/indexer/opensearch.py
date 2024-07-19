from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.embeddings import Embeddings
from langchain.vectorstores.opensearch_vector_search import OpenSearchVectorSearch

from semantic_ai.indexer.base import BaseIndexer
from semantic_ai.utils import check_isfile, iter_to_aiter, sync_to_async


class OpensearchIndexer(BaseIndexer):
    def __init__(
            self,
            *,
            url: str,
            index_name: str,
            user: str | None = None,
            password: str | None = None,
            embedding: Embeddings | None = HuggingFaceEmbeddings(),
            **kwargs
    ):
        self.url = url
        self.index_name = index_name
        self.user = user
        self.password = password
        self.embedding = embedding
        self.kwargs = kwargs
        self.opensearch = OpenSearchVectorSearch(
            opensearch_url=self.url,
            index_name=self.index_name,
            http_auth=(self.user, self.password),
            embedding_function=self.embedding,
            **self.kwargs
        )
        self._conn = self.opensearch.client

    async def create(self) -> OpenSearchVectorSearch:
        return OpenSearchVectorSearch(
            opensearch_url=self.url,
            index_name=self.index_name,
            http_auth=(self.user, self.password),
            embedding_function=self.embedding,
            **self.kwargs
        )

    async def index(self, extracted_json_dir_or_file: str, recursive: bool = False):
        if extracted_json_dir_or_file:
            documents_data = self.from_documents(extracted_json_dir_or_file, recursive)
            documents = await documents_data.asend(None)
            if await check_isfile(extracted_json_dir_or_file):
                try:
                    if documents:
                        await OpenSearchVectorSearch.afrom_documents(
                            opensearch_url=self.url,
                            http_auth=(self.user, self.password),
                            documents=documents,
                            index_name=f"{self.index_name}",
                            embedding=self.embedding,
                            **self.kwargs
                        )
                except Exception as ex:
                    print(f"{ex}")

            else:
                try:
                    async for docs in iter_to_aiter(documents):
                        if docs:
                            await OpenSearchVectorSearch.afrom_documents(
                                opensearch_url=self.url,
                                http_auth=(self.user, self.password),
                                documents=docs,
                                index_name=f"{self.index_name}",
                                embedding=self.embedding,
                                **self.kwargs
                            )
                except Exception as ex:
                    print(f"{ex}")
        else:
            raise ValueError(f"Please give valid file or directory path.")

    async def exists(self, index_name: str) -> bool:
        exist_index = await sync_to_async(
            self._conn.indices.exists,
            index=index_name
        )
        return exist_index

    async def delete(self, index_name: str):
        if await self.exists(index_name):
            await sync_to_async(
                self._conn.indices.delete,
                index=index_name
            )
            return True
        else:
            return False
