from aiopath import AsyncPath

from typing import (
    Optional
)

from langchain.embeddings.base import Embeddings
from langchain.vectorstores import ElasticsearchStore
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from semantic_ai.indexer.base import BaseIndexer
from semantic_ai.utils import file_process, check_isfile, iter_to_aiter


class ElasticsearchIndexer(BaseIndexer):

    def __init__(
            self,
            *,
            url: str,
            es_user: str | None = None,
            es_password: str | None = None,
            index_name: str,
            embedding: Optional[Embeddings] = HuggingFaceEmbeddings(),
            ssl_verify: bool = True
    ):
        super().__init__()
        self.url = url
        self.es_user = es_user
        self.es_password = es_password
        self.index_name = index_name
        self.embeddings = embedding
        self.ssl_verify = {"verify_certs": ssl_verify}

    async def create(self) -> ElasticsearchStore:
        obj = ElasticsearchStore(
            embedding=self.embeddings,
            es_url=self.url,
            es_user=self.es_user,
            es_password=self.es_password,
            index_name=f"{self.index_name}",
        )
        return obj

    @staticmethod
    async def from_documents(extracted_json_dir):
        if extracted_json_dir:
            datas = []
            dir_path = AsyncPath(extracted_json_dir)
            if await dir_path.is_file():
                file_path = str(dir_path)
                file_ext = dir_path.suffix.lower()
                data = await file_process(file_ext=file_ext, file_path=file_path)
                return data
            elif await dir_path.is_dir():
                async for path in dir_path.iterdir():
                    if await path.is_file():
                        file_path = str(path)
                        file_ext = path.suffix.lower()
                        _data = await file_process(file_ext=file_ext, file_path=file_path)
                        datas.append(_data)
                    else:
                        pass
                return datas
        else:
            raise ValueError(f"Please give valid file or directory path.")

    async def index(self, extracted_json_dir: str):
        if extracted_json_dir:
            documents = await self.from_documents(extracted_json_dir)
            if await check_isfile(extracted_json_dir):
                try:
                    await ElasticsearchStore.afrom_documents(
                        documents=documents,
                        embedding=self.embeddings,
                        es_url=self.url,
                        es_user=self.es_user,
                        es_password=self.es_password,
                        index_name=self.index_name
                    )
                except Exception as ex:
                    print(f"{ex}")
            else:
                try:
                    async for docs in iter_to_aiter(documents):
                        await ElasticsearchStore.afrom_documents(
                            documents=docs,
                            embedding=self.embeddings,
                            es_url=self.url,
                            es_user=self.es_user,
                            es_password=self.es_password,
                            index_name=self.index_name
                        )
                except Exception as ex:
                    print(f"{ex}")
        else:
            raise ValueError(f"Please give valid file or directory path.")
