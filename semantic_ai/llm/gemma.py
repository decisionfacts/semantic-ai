import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from semantic_ai.llm.base import BaseLLM
from semantic_ai.utils import sync_to_async
from semantic_ai.constants import DEFAULT_PROMPT


class Gemma(BaseLLM):

    def __init__(self,
                 *,
                 model_name_or_path: str,
                 device_map: str | None = "auto",
                 torch_dtype: str | torch.dtype = torch.float16,
                 do_sample: bool = True,
                 attn_implementation: str | None = None,
                 load_in_4bit: bool = False,
                 model_kwargs: Optional[Dict[str, Any]] = None,
                 max_length: int = 400,
                 **kwargs
                 ):
        self.model_name_or_path = model_name_or_path
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        self.attn_implementation = attn_implementation
        self.load_in_4bit = load_in_4bit
        self.max_length = max_length
        self.do_sample = do_sample

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, **kwargs)
        # Normal model config
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path,
                                                          device_map=self.device_map,
                                                          torch_dtype=self.torch_dtype,
                                                          **kwargs
                                                          )

        # Flash Attention 2 config
        if self.attn_implementation:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name_or_path,
                device_map=self.device_map,
                torch_dtype=self.torch_dtype,
                attn_implementation=self.attn_implementation,
                **kwargs
            )

        # bitsandbytes-4bit config
        if self.load_in_4bit:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name_or_path,
                device_map=self.device_map,
                load_in_4bit=self.load_in_4bit,
                **kwargs
            )

        self._pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            eos_token_id=self.tokenizer.eos_token_id,
            model_kwargs=model_kwargs,
            **kwargs
        )

    async def prompt_generate(self, question: str, prompt_template: str = DEFAULT_PROMPT, context: List[str] = None):
        pass

    async def llm_model(self, prompt: str = DEFAULT_PROMPT):
        asyncio.create_task(_clear_cache())
        return await sync_to_async(self._pipe,
                                   prompt,
                                   do_sample=self.do_sample,
                                   max_length=self.max_length,
                                   eos_token_id=self.tokenizer.eos_token_id,
                                   truncation=True
                                   )
