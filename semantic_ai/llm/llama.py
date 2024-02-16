import asyncio
import logging
from typing import Any, Dict, Optional

import torch
from df_extract.utils import sync_to_async
from transformers import (
    pipeline,
    LlamaForCausalLM,
    LlamaTokenizer
)

from semantic_ai.llm.base import BaseLLM
from semantic_ai.utils import _clear_cache

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_DEVICE = ["cpu", "cuda", "auto"]


class Llama(BaseLLM):

    def __init__(self,
                 *,
                 model_name_or_path: str,
                 torch_dtype: str | torch.dtype = torch.float16,
                 do_sample: bool = True,
                 model_kwargs: Optional[Dict[str, Any]] = None,
                 max_length: int = 400,
                 device: str | None = None,
                 **kwargs
                 ):
        self.model_name_or_path = model_name_or_path
        self.do_sample = do_sample
        self.max_length = max_length
        self.device = device

        if self.device and self.device not in DEFAULT_DEVICE:
            raise ValueError(f"Only given the following device{DEFAULT_DEVICE}")
        if not self.device:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available():
            torch_dtype = torch.bfloat16
        self.model = LlamaForCausalLM.from_pretrained(self.model_name_or_path,
                                                      device_map=self.device,
                                                      trust_remote_code=True,
                                                      torch_dtype=torch_dtype,
                                                      **kwargs)
        self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name_or_path,
                                                        **kwargs)
        self._pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            eos_token_id=self.tokenizer.eos_token_id,
            torch_dtype=torch_dtype,
            device_map=self.device,
            model_kwargs=model_kwargs,
            **kwargs
        )

    async def llm_model(self, prompt):
        asyncio.create_task(_clear_cache())
        return await sync_to_async(self._pipe,
                                   prompt,
                                   do_sample=self.do_sample,
                                   max_length=self.max_length,
                                   eos_token_id=self.tokenizer.eos_token_id,
                                   truncation=True
                                   )

    class LlamaGptq(BaseLLM):

        def __init__(self):
            pass

        async def llm_model(self):
            raise NotImplementedError
