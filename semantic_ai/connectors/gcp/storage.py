from abc import ABC

from google.cloud import storage
from google.oauth2 import service_account

from semantic_ai.utils import sync_to_async
from semantic_ai.connectors.base import BaseConnectors


class GCPStorage(BaseConnectors, ABC):

    async def connect(self, info, bucket_name):

        if isinstance(info, str):
            credentials = service_account.Credentials.from_service_account_file(info)
        elif isinstance(info, dict):
            credentials = service_account.Credentials.from_service_account_info(info)
        else:
            raise ValueError(f"{info} is not supported type. Please give json format or give json file path as string")

        storage_client = storage.Client(
            credentials=credentials
        )
        return await sync_to_async(storage_client.get_bucket,
                                   bucket_or_name=bucket_name
                                   )
