import asyncio
import sys
sys.path.insert(0, '/home/suhkth/Desktop/Rag/agentic_rag_app/backend')

from app.services.openai_service import create_thread

async def test():
    try:
        thread_id = await create_thread()
        print(f"✅ Success! Thread created: {thread_id}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
