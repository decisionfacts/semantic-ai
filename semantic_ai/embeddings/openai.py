from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

from langchain.pydantic_v1 import Field
from semantic_ai.embeddings.base import BaseEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings as OpenAI_Embed


class OpenAIEmbeddings(BaseEmbeddings):
    """OpenAI embedding models.

        To use, you should have the ``openai`` python package installed, and the
        environment variable ``OPENAI_API_KEY`` set with your API key or pass it
        as a named parameter to the constructor.

        Example:
            . code-block:: python

                from semantic.embeddings.openai import OpenAIEmbeddings
                openai = OpenAIEmbeddings(openai_api_key="my-api-key")
        """

    client: Any = None  #: :meta private:
    model_name: str = "text-embedding-ada-002"
    embedding_ctx_length: int = 8191
    """The maximum number of tokens to embed at once."""
    openai_api_key: Optional[str] = None
    chunk_size: int = 1000
    """Maximum number of texts to embed in each batch"""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout in seconds for the OpenAPI request."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""

    def __init__(
            self, **kwargs
    ):
        super().__init__(**kwargs)

    async def embed(self):
        embeddings = OpenAI_Embed(
            client=self.client,
            model=self.model_name,
            embedding_ctx_length=self.embedding_ctx_length,
            openai_api_key=self.openai_api_key,
            chunk_size=self.chunk_size,
            max_retries=self.max_retries,
            request_timeout=self.request_timeout,
            model_kwargs=self.model_kwargs
        )
        return embeddings
