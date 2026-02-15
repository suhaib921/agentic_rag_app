import tiktoken
from pypdf import PdfReader
from docx import Document
from langsmith import traceable
from app.db.supabase import get_supabase_client
from app.services.embeddings import generate_embeddings_batch

@traceable(name="extract_text")
async def extract_text(file_path: str, file_type: str) -> str:
    """Extract text from document based on file type."""
    if file_type == "pdf":
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages)
    elif file_type == "docx":
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    elif file_type in ["txt", "md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

@traceable(name="chunk_text")
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """Chunk text into fixed-size pieces with overlap."""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append({
            "content": chunk_text,
            "chunk_index": len(chunks),
            "metadata": {
                "start_token": start,
                "end_token": end,
                "token_count": len(chunk_tokens)
            }
        })

        start += (chunk_size - overlap)

    return chunks

@traceable(name="process_document")
async def process_document(document_id: str, user_id: str):
    """Full ingestion pipeline for a document."""
    supabase = get_supabase_client()

    try:
        # Get document record
        doc = supabase.table("documents").select("*").eq("id", document_id).single().execute()
        doc_data = doc.data

        # Update status: processing
        supabase.table("documents").update({"status": "processing"}).eq("id", document_id).execute()

        # Download file from storage
        file_bytes = supabase.storage.from_("documents").download(doc_data["storage_path"])
        local_path = f"/tmp/{document_id}_{doc_data['filename']}"
        with open(local_path, "wb") as f:
            f.write(file_bytes)

        # Extract text
        text = await extract_text(local_path, doc_data["file_type"])

        # Update status: chunking
        supabase.table("documents").update({"status": "chunking"}).eq("id", document_id).execute()

        # Chunk text
        chunks = chunk_text(text)

        # Update status: embedding
        supabase.table("documents").update({"status": "embedding"}).eq("id", document_id).execute()

        # Generate embeddings in batches
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c["content"] for c in batch]
            embeddings = await generate_embeddings_batch(texts)

            # Insert chunks into database
            chunk_records = [
                {
                    "document_id": document_id,
                    "user_id": user_id,
                    "content": chunk["content"],
                    "chunk_index": chunk["chunk_index"],
                    "embedding": embedding,
                    "metadata": chunk["metadata"]
                }
                for chunk, embedding in zip(batch, embeddings)
            ]
            supabase.table("chunks").insert(chunk_records).execute()

        # Update status: completed
        supabase.table("documents").update({
            "status": "completed",
            "chunk_count": len(chunks)
        }).eq("id", document_id).execute()

    except Exception as e:
        # Update status: failed
        supabase.table("documents").update({
            "status": "failed",
            "error_message": str(e)
        }).eq("id", document_id).execute()
        raise
