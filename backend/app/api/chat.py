from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.auth.middleware import verify_token
from app.models.schemas import ThreadCreate, ThreadResponse, MessageResponse
from app.services.openai_service import create_thread, send_message_stream
from app.services.langsmith_service import traced_stream
from supabase import create_client, Client, ClientOptions
from app.config import settings
import json
from typing import AsyncIterator

router = APIRouter(prefix="/api/chat", tags=["chat"])

def get_supabase_client(token: str) -> Client:
    """Create Supabase client with user's JWT token for RLS."""
    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
        options=ClientOptions(headers={"Authorization": f"Bearer {token}"})
    )

@router.post("/threads", response_model=ThreadResponse)
async def create_chat_thread(
    thread_data: ThreadCreate = ThreadCreate(),
    user_info: dict = Depends(verify_token)
):
    """Create new chat thread."""
    try:
        supabase = get_supabase_client(user_info["token"])
        openai_thread_id = await create_thread()

        result = supabase.table("threads").insert({
            "user_id": user_info["user_id"],
            "openai_thread_id": openai_thread_id,
            "title": thread_data.title or "New Chat"
        }).execute()

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threads", response_model=list[ThreadResponse])
async def get_threads(user_info: dict = Depends(verify_token)):
    """Get all user threads."""
    try:
        supabase = get_supabase_client(user_info["token"])
        result = supabase.table("threads")\
            .select("*")\
            .eq("user_id", user_info["user_id"])\
            .order("updated_at", desc=True)\
            .execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threads/{thread_id}/messages", response_model=list[MessageResponse])
async def get_messages(thread_id: str, user_info: dict = Depends(verify_token)):
    """Get thread messages."""
    try:
        supabase = get_supabase_client(user_info["token"])

        # Verify ownership
        thread = supabase.table("threads")\
            .select("*")\
            .eq("id", thread_id)\
            .eq("user_id", user_info["user_id"])\
            .single()\
            .execute()

        if not thread.data:
            raise HTTPException(status_code=404, detail="Thread not found")

        result = supabase.table("messages")\
            .select("*")\
            .eq("thread_id", thread_id)\
            .order("created_at")\
            .execute()

        return result.data
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] get_messages failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/threads/{thread_id}/messages/stream")
async def send_message(
    thread_id: str,
    content: str,
    user_info: dict = Depends(verify_token)
):
    """Send message, stream response."""
    try:
        supabase = get_supabase_client(user_info["token"])

        # Verify ownership
        thread = supabase.table("threads")\
            .select("*")\
            .eq("id", thread_id)\
            .eq("user_id", user_info["user_id"])\
            .single()\
            .execute()

        if not thread.data:
            raise HTTPException(status_code=404, detail="Thread not found")

        openai_thread_id = thread.data["openai_thread_id"]

        # Store user message
        supabase.table("messages").insert({
            "thread_id": thread_id,
            "user_id": user_info["user_id"],
            "role": "user",
            "content": content
        }).execute()

        async def stream_generator() -> AsyncIterator[bytes]:
            assistant_content = ""

            # Stream from OpenAI with LangSmith tracing
            stream_gen = send_message_stream(openai_thread_id, content)

            async for chunk in traced_stream(
                openai_thread_id,
                content,
                user_info["user_id"],
                stream_gen
            ):
                assistant_content += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n".encode()

            # Store assistant message
            supabase.table("messages").insert({
                "thread_id": thread_id,
                "user_id": user_info["user_id"],
                "role": "assistant",
                "content": assistant_content
            }).execute()

            # Update thread timestamp
            supabase.table("threads")\
                .update({"updated_at": "now()"})\
                .eq("id", thread_id)\
                .execute()

            yield f"data: {json.dumps({'done': True})}\n\n".encode()

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
