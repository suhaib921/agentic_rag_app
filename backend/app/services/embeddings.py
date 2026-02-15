from openai import AsyncOpenAI
from langsmith import traceable
from app.config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

@traceable(name="generate_embedding")
async def generate_embedding(text: str) -> list[float]:
    """Generate embedding vector for text using OpenAI."""
    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )
    return response.data[0].embedding

@traceable(name="generate_embeddings_batch")
async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for multiple texts in a single API call."""
    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=texts
    )
    return [item.embedding for item in response.data]
