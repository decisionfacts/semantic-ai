import logging

from semantic_ai.llm.base import BaseLLM

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def _model_type():
    model_list = []
    for model in ModelTypes:
        value = model.value
        model_list.append(value)
    return model_list


DEFAULT_PARAMETERS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 500
}


class Ibm(BaseLLM):

    def __init__(self,
                 *,
                 url: str,
                 api_key: str,
                 project_id: str,
                 model_type: str | None = None,
                 parameters: dict | None = None
                 ):
        self.url = url
        self.api_key = api_key
        self.project_id = project_id
        self.model_type = model_type or ModelTypes.LLAMA_2_70B_CHAT.value
        self.parameters = parameters or DEFAULT_PARAMETERS

        if not self.url:
            raise ValueError(f"Url has empty. Please provide valid url")
        if not self.api_key:
            raise ValueError(f"Api key has empty. Please provide valid api key")
        if not self.project_id:
            raise ValueError(f"Project id has empty. Please provide valid project id")
        self.ibm_llm_credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
        model_type_list = _model_type()
        print(self.model_type)
        if self.model_type not in model_type_list:
            raise ValueError(
                f"{self.model_type} not in the model type list. Please give the following model type: {model_type_list}"
            )

    async def llm_model(self):
        ibm_llm_model = Model(
            model_id=self.model_type,
            credentials=self.ibm_llm_credentials,
            project_id=self.project_id,
            params=self.parameters
        )
        logger.info("ibm_llm_model_loaded->%s" % ibm_llm_model.get_details()['short_description'])
        ibm_llm = ibm_llm_model.to_langchain()
        return ibm_llm
