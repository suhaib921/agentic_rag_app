from langsmith import Client
from langsmith.run_helpers import traceable
from app.config import settings
from typing import AsyncIterator

langsmith_client = Client(api_key=settings.langsmith_api_key)

@traceable(
    run_type="llm",
    project_name=settings.langsmith_project,
    client=langsmith_client
)
async def traced_stream(
    thread_id: str,
    content: str,
    user_id: str,
    stream_gen: AsyncIterator[str]
) -> AsyncIterator[str]:
    """Wrapper that traces OpenAI streaming to LangSmith."""
    full_response = ""

    async for chunk in stream_gen:
        full_response += chunk
        yield chunk

    # @traceable automatically logs input/output
