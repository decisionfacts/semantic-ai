import asyncio
import os
from abc import ABCMeta, abstractmethod

from aiopath import AsyncPath

from semantic_ai.utils import file_process, sync_to_async, iter_to_aiter


class BaseIndexer(metaclass=ABCMeta):

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

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def index(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def exists(self, index_name: str):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, index_name: str):
        raise NotImplementedError
