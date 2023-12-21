import time

import aiofiles
import httpx
import os
import logging

from semantic_ai.connectors.base import BaseConnectors
from semantic_ai.constants import DEFAULT_FOLDER_NAME
from semantic_ai.utils import sync_to_async, iter_to_aiter, recursive_dir, empty_folder

MICROSOFT_OAUTH_URL = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
SITE_URL = "https://graph.microsoft.com/v1.0/sites"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_path(url):
    index = url.find('PowerAppsProd')
    if index != -1:
        index = url.find('PowerAppsProd')
        return url[index + len('PowerAppsProd') + 1:]
    else:
        index = url.find('Documents')
        return url[index + len('Documents') + 1:]


class Sharepoint(BaseConnectors):

    def __init__(
            self,
            *,
            client_id: str,
            client_secret: str,
            scope: str,
            tenant_id: str,
            host_name: str,
            grant_type: str | None = None,
            output_dir: str | None = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type or "client_credentials"
        self.output_dir = output_dir
        self.scope = scope
        self.tenant_id = tenant_id
        self.host_name = host_name

        if not self.output_dir:
            dir_path = os.getcwd().split('/')
            download_path = "/".join(dir_path)
            self.output_dir = f"{download_path}/{DEFAULT_FOLDER_NAME}"
        is_exist = os.path.exists(self.output_dir)
        if not is_exist:
            os.makedirs(self.output_dir)
        logger.info(f"file download output dir created {self.output_dir}")

    async def connect(self, site_name) -> dict:
        site_id_url = f"{SITE_URL}/{self.host_name}:/sites/{site_name}"
        site_object = await self.__make_request(site_id_url)
        return site_object

    async def __make_request(self, url):
        headers = {
            'Authorization': 'Bearer {}'.format(await self.__get_access_token())
        }
        async with httpx.AsyncClient() as cli:
            r = await cli.get(url, headers=headers, timeout=30)
        return await sync_to_async(r.json)

    async def __get_access_token(self):
        token_request_uri = MICROSOFT_OAUTH_URL.format(self.tenant_id)
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type,
            'scope': self.scope
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                token_request_uri,
                data=data,
            )
        token_response = await sync_to_async(resp.json)
        if token_response.get('error'):
            raise ValueError(token_response.get('error_description'))
        access_token = token_response.get('access_token')
        return access_token

    async def list_drives(self, site_id):
        drive_uri = f'{SITE_URL}/{site_id}/drives'
        drives = await self.__make_request(drive_uri)
        return drives

    async def list_folders(self, site_id, drive_id):
        folder_list_url = f"{SITE_URL}/{site_id}/drives/{drive_id}/root/children"
        folder = await self.__make_request(folder_list_url)
        return folder

    async def list_sites(self):
        sites = await self.__make_request(SITE_URL)
        return sites

    @staticmethod
    async def file_download(file_name, file_download, file_path):
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', file_download) as resp:
                save_to_path = os.path.join(file_path, file_name)
                async with aiofiles.open(save_to_path, "wb") as f:
                    async for chunk in resp.aiter_bytes():
                        await f.write(chunk)

    async def __make_api(self, uri, site_id, drive_id, recursive):
        items_uri = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{uri}:/children'
        items = await self.__make_request(items_uri)
        await self.iterate_items(items, site_id, drive_id, recursive)

    async def iterate_items(self, items, site_id, drive_id, recursive: bool):
        async for file in iter_to_aiter(items.get('value', [])):
            folder = file.get('folder')
            folder_url = file.get('webUrl')
            parent_ref = file.get('parentReference').get('path')
            parent_dir = parent_ref.split('/root:/')[-1]
            if folder is None:
                file_name = file.get('name')
                dir_path = f"{self.output_dir}/{parent_dir}"
                async with aiofiles.open(f"{self.output_dir}/file_list.txt", 'a') as file_list:
                    await file_list.write(f"File Name: {file_name} - Dir: {dir_path}\n")
                await recursive_dir(dir_path)
                file_download = file.get('@microsoft.graph.downloadUrl')
                await self.file_download(file_name, file_download, dir_path)
            elif folder and recursive:
                folder_name = file.get('name')
                _dir_path = f"{self.output_dir}/{parent_dir}/{folder_name}"
                await recursive_dir(_dir_path)
                path = await get_path(folder_url)
                await self.__make_api(path, site_id, drive_id, recursive)

    async def download(
            self,
            site_id,
            drive_id,
            folder_url: str = None,
            recursive: bool = False
    ):
        if not folder_url:
            raise ValueError(f"Please give valid folder url path for which folder download. e.g. /Myfolder/child/")
        try:
            url = folder_url.strip('/')
            folder_url = f"{SITE_URL}/{site_id}/drives/{drive_id}/root:/{url}:/children"
            items = await self.__make_request(folder_url)
            logger.info(f"Downloading started. Please check in {self.output_dir} dir")
            _download = await self.iterate_items(items, site_id, drive_id, recursive)
            logger.info(f"Files are downloaded in {self.output_dir} dir")
            logger.info(f"Empty folder checking and writing in {self.output_dir}/{url}")
            await empty_folder(f"{self.output_dir}/{url}", self.output_dir)
            logger.info(f"Process Completed")
        except Exception as ex:
            print(ex)
            logger.info(f"Download failed")
            logger.error(f"Sharepoint download error: {ex}")
