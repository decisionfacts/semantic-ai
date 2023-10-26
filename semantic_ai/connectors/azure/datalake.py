from abc import ABC

from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import DataLakeDirectoryClient
from azure.storage.filedatalake import DataLakeFileClient
from azure.storage.filedatalake import FileSystemClient

from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient

from semantic_ai.utils import sync_to_async
from semantic_ai.connectors.base import BaseConnectors


class AzureDataLake(BaseConnectors, ABC):

    def __init__(self,
                 account_name: str,
                 account_key: str
                 ):
        self.account_name = account_name
        self.account_key = account_key

    async def connect(self):
        return await self._get_conn_str()

    async def _get_conn_str(self):
        connect_str = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};" \
                      f"AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        return connect_str

    async def connect_service_client(self) -> DataLakeServiceClient:
        connect_str = await self._get_conn_str()
        return await sync_to_async(DataLakeServiceClient.from_connection_string, connect_str)

    async def connect_file_system_client(self, file_system_name: str) -> FileSystemClient:
        connect_str = await self._get_conn_str()
        conn = await sync_to_async(DataLakeServiceClient.from_connection_string, connect_str)
        return await sync_to_async(conn.get_file_system_client, file_system_name)

    async def connect_directory_client(self,
                                       container_name: str,
                                       directory_name: str
                                       ) -> DataLakeDirectoryClient:
        connect_str = await self._get_conn_str()
        return await sync_to_async(
            DataLakeDirectoryClient.from_connection_string,
            connect_str,
            container_name,
            directory_name
        )

    async def connect_file_client(self,
                                  container_name: str,
                                  directory_name: str,
                                  file_path: str
                                  ) -> DataLakeFileClient:
        connect_str = await self._get_conn_str()
        return await sync_to_async(
            DataLakeFileClient.from_connection_string,
            connect_str,
            container_name,
            directory_name,
            file_path
        )

    async def connect_table_service_client(self) -> TableServiceClient:
        connect_str = await self._get_conn_str()
        return await sync_to_async(
            TableServiceClient.from_connection_string,
            connect_str
        )

    async def connect_table_client(self, table_name: str) -> TableClient:
        connect_str = await self._get_conn_str()
        return await sync_to_async(
            TableClient.from_connection_string,
            connect_str,
            table_name=table_name
        )
