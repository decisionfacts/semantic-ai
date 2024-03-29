import asyncio
import os
from typing import (
    Optional
)

from aiopath import AsyncPath
from elasticsearch import Elasticsearch
from langchain.embeddings.base import Embeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import ElasticsearchStore

from semantic_ai.indexer.base import BaseIndexer
from semantic_ai.utils import file_process, check_isfile, iter_to_aiter, sync_to_async


class ElasticsearchIndexer(BaseIndexer):

    def __init__(
            self,
            *,
            url: str,
            es_user: str | None = None,
            es_password: str | None = None,
            index_name: str,
            embedding: Optional[Embeddings] = HuggingFaceEmbeddings(),
            verify_certs: bool = True,
            es_api_key: Optional[str] = None,
            **kwargs
    ):
        super().__init__()
        self.url = url
        self.es_user = es_user
        self.es_password = es_password
        self.index_name = index_name
        self.embeddings = embedding
        self.verify_certs = verify_certs
        self.es_api_key = es_api_key
        self.kwargs = kwargs

        self.es_connection = Elasticsearch(self.url,
                                           basic_auth=(self.es_user, self.es_password),
                                           verify_certs=self.verify_certs,
                                           **kwargs
                                           )

    async def create(self) -> ElasticsearchStore:
        obj = ElasticsearchStore(
            embedding=self.embeddings,
            index_name=f"{self.index_name}",
            es_connection=self.es_connection,
            es_api_key=self.es_api_key,
            **self.kwargs
        )
        return obj

    @staticmethod
    async def from_documents(extracted_json_dir, recursive: bool):
        if extracted_json_dir:
            datas = []
            dir_path = AsyncPath(extracted_json_dir)
            if await dir_path.is_file():
                file_path = str(dir_path)
                file_ext = dir_path.suffix.lower()
                data = await file_process(file_ext=file_ext, file_path=file_path)
                await asyncio.sleep(1)
                yield data
            elif await dir_path.is_dir():
                if recursive:
                    walk_dir = await sync_to_async(os.walk, dir_path)
                    async for root, dirs, files in iter_to_aiter(walk_dir):
                        for file in files:
                            path = AsyncPath(f"{root}/{file}")
                            file_path = str(path)
                            file_ext = path.suffix.lower()
                            _data = await file_process(file_ext=file_ext, file_path=file_path)
                            datas.append(_data)
                        else:
                            pass
                    await asyncio.sleep(1)
                    yield datas
                else:
                    async for path in dir_path.iterdir():
                        if await path.is_file():
                            file_path = str(path)
                            file_ext = path.suffix.lower()
                            _data = await file_process(file_ext=file_ext, file_path=file_path)
                            datas.append(_data)
                        else:
                            pass
                    yield datas
        else:
            raise ValueError(f"Please give valid file or directory path.")

    async def index(self, extracted_json_dir_or_file: str, recursive: bool = False):
        if extracted_json_dir_or_file:
            documents_data = self.from_documents(extracted_json_dir_or_file, recursive)
            documents = await documents_data.asend(None)
            if await check_isfile(extracted_json_dir_or_file):
                try:
                    if documents:
                        await ElasticsearchStore.afrom_documents(
                            documents=documents,
                            embedding=self.embeddings,
                            index_name=self.index_name,
                            es_connection=self.es_connection,
                            **self.kwargs

                        )
                except Exception as ex:
                    print(f"{ex}")
            else:
                try:
                    async for docs in iter_to_aiter(documents):
                        if docs:
                            await ElasticsearchStore.afrom_documents(
                                documents=docs,
                                embedding=self.embeddings,
                                index_name=self.index_name,
                                es_connection=self.es_connection,
                                **self.kwargs
                            )
                except Exception as ex:
                    print(f"{ex}")
        else:
            raise ValueError(f"Please give valid file or directory path.")

    async def exists(self, index_name: str) -> bool:
        exist_index = await sync_to_async(
            self.es_connection.indices.exists,
            index=index_name
        )
        return exist_index

    async def delete(self, index_name: str):
        if await self.exists(index_name):
            await sync_to_async(
                self.es_connection.indices.delete,
                index=index_name
            )
            return True
        else:
            return False
