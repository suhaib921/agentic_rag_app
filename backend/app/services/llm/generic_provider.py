from openai import AsyncOpenAI
from langsmith import traceable
from .base import BaseLLMProvider

class GenericProvider(BaseLLMProvider):
    """For Ollama, LM Studio, or any OpenAI-compatible endpoint."""

    def __init__(self, base_url: str, api_key: str = "not-needed"):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key
        )

    @traceable(name="generic_stream_chat")
    async def stream_chat(self, messages, model):
        # Same implementation
        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield {
                    "type": "text_delta",
                    "content": chunk.choices[0].delta.content
                }
        yield {"type": "done"}

    @traceable(name="generic_chat")
    async def chat(self, messages, model):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
