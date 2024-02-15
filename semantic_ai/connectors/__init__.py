from semantic_ai.connectors.microsoft.sharepoint import Sharepoint
from semantic_ai.connectors.mysql import Mysql
from semantic_ai.connectors.sqlite import Sqlite
from semantic_ai.constants import CONNECTORS_LIST
from semantic_ai.utils import get_dynamic_class

__all__ = [
    'Sharepoint',
    'Sqlite',
    'Mysql',
    'get_connectors'
]


async def get_connectors(connector_type: str, **kwargs):
    if connector_type not in CONNECTORS_LIST:
        raise ValueError(f"Please give the below following connector type.{CONNECTORS_LIST}")
    connector_cls = await get_dynamic_class(
        class_name=f"{connector_type.capitalize()}",
        module_name=f"semantic_ai.connectors"
    )
    return connector_cls(**kwargs)
