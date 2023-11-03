import asyncio
import functools
import importlib
import os

from concurrent.futures import ThreadPoolExecutor
from typing import List
from aiopath import AsyncPath

from langchain.document_loaders import JSONLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.schema.document import Document


async def sync_to_async(func, *args, **kwargs):
    """
    Utility function to convert sync function to async

    :param func: Valid callable
    :param args: Input for callable arguments
    :param kwargs: Input for callable keyword arguments
    :return: Returns based on the callable
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, functools.partial(func, *args, **kwargs))


async def iter_to_aiter(iterable):
    """
    Utility function to convert sync iteration to async

    :param iterable:
    """
    for item in iterable:
        yield item


async def get_dynamic_class(class_name, module_name: str, package_name: str = None):
    cls_module = importlib.import_module(module_name, package=package_name)
    return getattr(cls_module, class_name, None)


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["page_number"] = record.get("number")
    if metadata.get('source'):
        raw_filename = metadata["source"].rsplit('/', 1)[1]
        if raw_filename:
            filename = raw_filename.rsplit('.', 1)[0]
            metadata["file_name"] = filename
            metadata['source'] = filename
    return metadata


async def file_process(file_ext, file_path) -> List[Document]:
    try:
        loader = None
        if file_ext in '.json':
            loader = JSONLoader(
                file_path=file_path,
                jq_schema='.[]',
                content_key="content",
                text_content=False,
                metadata_func=metadata_func)
        elif file_ext in '.csv':
            loader = CSVLoader(file_path)
        else:
            print(f"{file_ext} is not supported")
        if not loader:
            raise ValueError(f"Data has empty. Please give valid file path and ext")
        data = await sync_to_async(loader.load)
        if len(data) > 0:
            return data
    except Exception as ex:
        print(f"{ex}")


async def check_isfile(path):
    dir_path = AsyncPath(path)
    if await dir_path.is_file():
        return True
    else:
        return False


async def create_dir(path, folder_name):
    _dir_path = f"{path}/{folder_name}"
    is_exist = os.path.exists(_dir_path)
    if not is_exist:
        os.makedirs(_dir_path)
    return _dir_path


async def make_dirs(_dir_path, folder_name):
    if not _dir_path:
        dir_path = os.getcwd().split('/')
        download_path = "/".join(dir_path)
        _dir_path = f"{download_path}/{folder_name}"
    is_exist = os.path.exists(_dir_path)
    if not is_exist:
        os.makedirs(_dir_path)
    return _dir_path
