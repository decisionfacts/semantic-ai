import logging

import torch
from langchain import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, TextStreamer, StoppingCriteria, StoppingCriteriaList

from semantic_ai.llm.base import BaseLLM

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class KeywordsStoppingCriteria(StoppingCriteria):
    def __init__(self, keywords_ids: list):
        print("stop_ids", keywords_ids)
        self.stop_token_ids = keywords_ids

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in self.stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False


class Llama(BaseLLM):

    def __init__(self,
                 *,
                 model_name_or_path: str
                 ):
        device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
        if torch.cuda.is_available():
            from auto_gptq import AutoGPTQForCausalLM, exllama_set_max_input_length

            '''
            add Stop_words to stop text generation on junk values
            '''
            stop_list = ['\n```\n']
            stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
            stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]
            stop_criteria = KeywordsStoppingCriteria(stop_token_ids)
            gptq_model = AutoGPTQForCausalLM.from_quantized(
                model_name_or_path,
                model_basename="model",
                use_safetensors=True,
                device_map='auto',
                pad_token_id=tokenizer.eos_token_id,
                inject_fused_attention=False,
                early_stopping=True,
                use_triton=False
            )
            gptq_model = torch.compile(gptq_model)
            # gptq_model = exllama_set_max_input_length(gptq_model, 4096)
            gptq_model = exllama_set_max_input_length(gptq_model, 8192)
            gptq_model.eval()
            _pipe = pipeline("text-generation",
                             model=gptq_model,
                             tokenizer=tokenizer,
                             # torch_dtype=torch.float16,
                             torch_dtype="auto",
                             max_new_tokens=4096,
                             top_k=1,
                             temperature=0.1,
                             return_full_text=True,
                             top_p=0.5,
                             remove_invalid_values=True,
                             do_sample=True,
                             pad_token_id=tokenizer.eos_token_id,
                             eos_token_id=tokenizer.eos_token_id,
                             stopping_criteria=StoppingCriteriaList([stop_criteria]),
                             early_stopping=True,
                             clean_up_tokenization_spaces=True,
                             repetition_penalty=1.1,
                             streamer=TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
                             )
            self._llm = HuggingFacePipeline(pipeline=_pipe)
            logger.info("LLM Model Loaded")

    async def llm_model(self):
        return self._llm
