from abc import ABC

from google.cloud import bigquery
from google.oauth2 import service_account

from semantic_ai.connectors.base import BaseConnectors


class BigQuery(BaseConnectors, ABC):

    def connect(self, info):
        if isinstance(info, str):
            credentials = service_account.Credentials.from_service_account_file(info)
            return credentials
        elif isinstance(info, dict):
            credentials = service_account.Credentials.from_service_account_info(info)
            return credentials
        else:
            raise ValueError(f"{info} is not supported type. Please give json format or give json file path as string")
