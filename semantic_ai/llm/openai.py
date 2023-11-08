from typing import Optional

from semantic_ai.llm.base import BaseLLM
from langchain.llms import OpenAI

DEFAULT_MODEL = "text-davinci-003"


class Openai(BaseLLM):

    def __init__(self,
                 *,
                 model_name_or_path: str | None = None,
                 openai_api_key: Optional[str] = None,
                 **kwargs
                 ):
        self.model_name = model_name_or_path or DEFAULT_MODEL
        self.openai_api_key = openai_api_key

        self.llm = OpenAI(model_name=self.model_name,
                          openai_api_key=self.openai_api_key,
                          **kwargs
                          )

    async def llm_model(self):
        return self.llm
