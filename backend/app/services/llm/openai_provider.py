from openai import AsyncOpenAI
from langsmith import traceable
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    @traceable(name="openai_stream_chat")
    async def stream_chat(self, messages, model):
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

    @traceable(name="openai_chat")
    async def chat(self, messages, model):
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
