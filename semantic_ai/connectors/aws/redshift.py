from abc import ABC

import redshift_connector

from semantic_ai.connectors.base import BaseConnectors


class RedShift(BaseConnectors, ABC):

    def connect(self, host, port, user, password, database, *args, **kwargs):
        conn = redshift_connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port,
            *args,
            **kwargs
        )
        return conn
