from openai import AsyncOpenAI
from langsmith import traceable
from .base import BaseLLMProvider

class OpenRouterProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    @traceable(name="openrouter_stream_chat")
    async def stream_chat(self, messages, model):
        # Same implementation as OpenAI (uses ChatCompletions API)
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

    @traceable(name="openrouter_chat")
    async def chat(self, messages, model):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
