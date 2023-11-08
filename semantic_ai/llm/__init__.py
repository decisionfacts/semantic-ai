from semantic_ai.constants import LLM_LIST
from semantic_ai.utils import get_dynamic_class
from semantic_ai.llm.llama import Llama
from semantic_ai.llm.openai import Openai


__all__ = [
    "Llama",
    "Openai",
    "get_llm"
]


async def get_llm(llm: str, **kwargs):
    if llm not in LLM_LIST:
        raise ValueError(f"Please give the below following index type.{LLM_LIST}")
    indexer_cls = await get_dynamic_class(
        class_name=f"{llm.capitalize()}",
        module_name=f"semantic_ai.llm"
    )
    print(indexer_cls)
    return indexer_cls(**kwargs)
