import httpx, aiofiles, os
from abc import ABC

from semantic_ai.utils import sync_to_async, iter_to_aiter
from semantic_ai.connectors.base import BaseConnectors
from semantic_ai.constants import DEFAULT_FOLDER_NAME

MICROSOFT_OAUTH_URL = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
SITE_URL = "https://graph.microsoft.com/v1.0/sites"


class Sharepoint(BaseConnectors, ABC):

    def __init__(self,
                 *,
                 client_id: str,
                 client_secret: str,
                 scope: str,
                 tenant_id: str,
                 host_name: str,
                 grant_type: str = "client_credentials",
                 output_dir: str = None
                 ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.local_dir = output_dir
        self.scope = scope
        self.tenant_id = tenant_id
        self.host_name = host_name

        if not self.local_dir:
            dir_path = os.getcwd().split('/')
            download_path = "/".join(dir_path)
            self.local_dir = f"{download_path}/{DEFAULT_FOLDER_NAME}"
        isExist = os.path.exists(self.local_dir)
        if not isExist:
            os.makedirs(self.local_dir)

    async def connect(self, site_name) -> dict:
        site_id_url = f"{SITE_URL}/{self.host_name}:/sites/{site_name}"
        site_object = await self.__make_request(site_id_url)
        return site_object

    async def __make_request(self, url):
        headers = {
            'Authorization': 'Bearer {}'.format(await self.__get_access_token())
        }
        async with httpx.AsyncClient() as cli:
            r = await cli.get(url, headers=headers)
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

    async def file_download(self, file_name, file_download):
        async with httpx.AsyncClient() as client:
            response = await client.get(file_download)
        save_to_path = os.path.join(self.local_dir, file_name)
        async with aiofiles.open(save_to_path, "wb") as f:
            await f.write(response.content)

    async def iterate_items(self, items):
        count = 0
        async for file in iter_to_aiter(items.get('value', [])):
            # if count < 1:
            folder = file.get('folder')
            if folder is None:
                file_name = file.get('name')
                file_download = file.get('@microsoft.graph.downloadUrl')
                await self.file_download(file_name, file_download)
            else:
                pass
            # count += 1
            # else:
            #     break

    async def download(self,
                       site_id,
                       drive_id,
                       folder_url: str = None,
                       ):
        if not folder_url:
            raise ValueError(f"Please give valid folder url path for which folder download. e.g. /Myfolder/child/")
        url = folder_url.strip('/')
        folder_url = f"{SITE_URL}/{site_id}/drives/{drive_id}/root:/{url}:/children"
        items = await self.__make_request(folder_url)
        await self.iterate_items(items)
