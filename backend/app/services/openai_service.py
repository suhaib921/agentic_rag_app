from openai import AsyncOpenAI
from app.config import settings
from typing import AsyncIterator

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def create_thread() -> str:
    """Create OpenAI thread, return thread_id."""
    thread = await client.beta.threads.create()
    return thread.id

async def send_message_stream(
    thread_id: str,
    content: str
) -> AsyncIterator[str]:
    """Send message to OpenAI thread, stream response."""
    # Add user message
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    # Stream response
    async with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=settings.openai_assistant_id
    ) as stream:
        async for event in stream:
            if event.event == 'thread.message.delta':
                for delta in event.data.delta.content:
                    if delta.type == 'text' and delta.text:
                        yield delta.text.value
