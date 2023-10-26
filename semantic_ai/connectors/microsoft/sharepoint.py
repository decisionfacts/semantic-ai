import httpx, aiofiles, os
from abc import ABC

from semantic_ai.utils import sync_to_async, iter_to_aiter
from semantic_ai.connectors.base import BaseConnectors
from semantic_ai.connectors.config import settings

MICROSOFT_OAUTH_URL = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"
SITE_URL = "https://graph.microsoft.com/v1.0/sites"
DEFAULT_FOLDER_NAME = "output"


class SharePoint(BaseConnectors, ABC):

    def __init__(self,
                 scope: str,
                 host_name: str = settings.SHARE_POINT_HOST_NAME,
                 client_id: str = settings.SHARE_POINT_CLIENT_ID,
                 client_secret: str = settings.SHARE_POINT_CLIENT_SECRET,
                 tenant_id: str = settings.SHARE_POINT_TENANT_ID,
                 grant_type: str = "client_credentials",
                 output_dir: str = None,
                 ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.local_dir = output_dir
        self.scope = scope
        self.tenant_id = tenant_id
        self.host_name = host_name

        if not self.local_dir:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.local_dir = f"{dir_path}/{DEFAULT_FOLDER_NAME}"
        isExist = os.path.exists(self.local_dir)
        if not isExist:
            os.makedirs(self.local_dir)

    async def connect(self, site_name):
        site_id_url = f"{SITE_URL}/{self.host_name}:/sites/{site_name}"
        site_object = await self.make_request(site_id_url)
        return site_object

    async def make_request(self, url):
        headers = {
            'Authorization': 'Bearer {}'.format(await self.get_access_token())
        }
        async with httpx.AsyncClient() as cli:
            r = await cli.get(url, headers=headers)
        return await sync_to_async(r.json)

    async def get_access_token(self):
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

    async def get_driver_id_list(self, site_id):
        drive_uri = f'{SITE_URL}/{site_id}/drives'
        drives = await self.make_request(drive_uri)
        return drives

    async def get_folder_list(self, site_id, drive_id):
        folder_list_url = f"{SITE_URL}/{site_id}/drives/{drive_id}/root/children"
        folder = await self.make_request(folder_list_url)
        return folder

    async def get_site_id_list(self):
        sites = await self.make_request(SITE_URL)
        return sites

    async def download_file(self, file_name, file_download):
        async with httpx.AsyncClient() as client:
            response = await client.get(file_download)
        save_to_path = os.path.join(self.local_dir, file_name)
        async with aiofiles.open(save_to_path, "wb") as f:
            await f.write(response.content)

    async def iterate_items(self, items):
        async for file in iter_to_aiter(items.get('value', [])):
            folder = file.get('folder')
            if folder is None:
                file_name = file.get('name')
                file_download = file.get('@microsoft.graph.downloadUrl')
                await self.download_file(file_name, file_download)
            else:
                pass

    async def file_download_specific_folder(self,
                                            site_id,
                                            drive_id,
                                            folder_name,
                                            ):
        folder_url = f"{SITE_URL}/{site_id}/drives/{drive_id}/root:/{folder_name}:/children"
        items = await self.make_request(folder_url)
        await self.iterate_items(items)
