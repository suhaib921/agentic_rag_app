from langsmith import traceable
from app.db.supabase import get_supabase_client
from app.services.embeddings import generate_embedding

@traceable(name="retrieve_context")
async def retrieve_context(query: str, user_id: str, top_k: int = 5) -> list[dict]:
    """Retrieve most relevant chunks for a query using vector similarity."""
    supabase = get_supabase_client()

    # Generate query embedding
    query_embedding = await generate_embedding(query)

    # Vector similarity search using pgvector
    # Note: This requires raw SQL for vector operations
    result = supabase.rpc(
        "match_chunks",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.5,
            "match_count": top_k,
            "user_id_filter": user_id
        }
    ).execute()

    return result.data

@traceable(name="format_context")
def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into context string for LLM."""
    if not chunks:
        return ""

    context_parts = ["Here are relevant excerpts from your documents:\n"]

    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"\n[Source {i}] (from {chunk.get('filename', 'Unknown')})\n"
            f"{chunk['content']}\n"
        )

    return "\n".join(context_parts)
