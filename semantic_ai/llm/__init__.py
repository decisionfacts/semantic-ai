from semantic_ai.constants import LLM_LIST
from semantic_ai.utils import get_dynamic_class
from semantic_ai.llm.llama import Llama
from semantic_ai.llm.openai import Openai
from semantic_ai.llm.ibm import Ibm

__all__ = [
    "Ibm",
    "Llama",
    "Openai",
    "get_llm"
]


def capitalize(name: str):
    if '-' not in name:
        return name.capitalize()
    else:
        split_name = name.split('-')
        name_list = [_name.capitalize() for _name in split_name]
        return ''.join(name_list)


async def get_llm(llm: str, **kwargs):
    if llm not in LLM_LIST:
        raise ValueError(f"Please give the below following index type.{LLM_LIST}")
    indexer_cls = await get_dynamic_class(
        class_name=f"{capitalize(llm)}",
        module_name=f"semantic_ai.llm"
    )
    print(indexer_cls)
    return indexer_cls(**kwargs)
