import logging
from typing import Optional

from semantic_ai.llm.base import BaseLLM
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI

DEFAULT_MODEL = "text-davinci-003"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Openai(BaseLLM):

    def __init__(self,
                 *,
                 model_name_or_path: str | None = None,
                 openai_api_key: Optional[str] = None,
                 **kwargs
                 ):
        self.model_name = model_name_or_path or DEFAULT_MODEL
        self.openai_api_key = openai_api_key

        try:
            if 'gpt' in self.model_name:
                logger.info(f"Chat Open AI model initiating")
                self.llm = ChatOpenAI(model_name=self.model_name,
                                      openai_api_key=self.openai_api_key,
                                      max_tokens=500,
                                      **kwargs
                                      )
            else:
                logger.info(f"Open AI model initiating")
                self.llm = OpenAI(model_name=self.model_name,
                                  openai_api_key=self.openai_api_key,
                                  **kwargs
                                  )
        except Exception as ex:
            logger.info(f"Open AI model failed to initiate {ex}")

    async def llm_model(self):
        try:
            _llm_model = self.llm
            return _llm_model
        except Exception as ex:
            logger.info(f"Open AI model failed to initiate {ex}")
