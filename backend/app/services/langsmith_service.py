import os
from langsmith import Client
from langsmith.run_helpers import traceable
from app.config import settings
from typing import AsyncIterator

# Enable LangSmith tracing
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_API_KEY'] = settings.langsmith_api_key
os.environ['LANGSMITH_PROJECT'] = settings.langsmith_project

langsmith_client = Client(api_key=settings.langsmith_api_key)

async def traced_stream(
    thread_id: str,
    content: str,
    user_id: str,
    stream_gen: AsyncIterator[str]
) -> AsyncIterator[str]:
    """Wrapper that traces OpenAI streaming to LangSmith."""
    full_response = ""

    # Stream chunks in real-time
    async for chunk in stream_gen:
        full_response += chunk
        yield chunk

    # Log to LangSmith after streaming completes
    try:
        langsmith_client.create_run(
            name="chat_stream",
            run_type="llm",
            inputs={"thread_id": thread_id, "user_message": content, "user_id": user_id},
            outputs={"assistant_response": full_response},
            project_name=settings.langsmith_project
        )
    except Exception as e:
        print(f"[WARN] LangSmith logging failed: {e}")
