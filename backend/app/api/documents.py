import os
import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.auth.middleware import verify_token
from app.db.supabase import get_supabase_client
from app.services.ingestion_service import process_document
from supabase import create_client, Client, ClientOptions
from app.config import settings

router = APIRouter(prefix="/api/documents", tags=["documents"])

def get_supabase_client_with_token(token: str) -> Client:
    """Create Supabase client with user's JWT token for RLS."""
    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
        options=ClientOptions(headers={"Authorization": f"Bearer {token}"})
    )

@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    user_info: dict = Depends(verify_token)
):
    """Upload a document and start processing."""
    supabase = get_supabase_client_with_token(user_info["token"])

    # Validate file type
    allowed_types = [
        "application/pdf",
        "text/plain",
        "text/markdown",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    if file.content_type not in allowed_types:
        # Also check file extension as fallback
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".txt", ".md", ".docx"]:
            raise HTTPException(400, "Unsupported file type")

    # Read file
    file_bytes = await file.read()
    file_size = len(file_bytes)

    # Determine file type from extension
    ext = os.path.splitext(file.filename)[1].lower()
    file_type_map = {".pdf": "pdf", ".txt": "txt", ".md": "md", ".docx": "docx"}
    file_type = file_type_map.get(ext, "txt")

    # Create document record
    doc_result = supabase.table("documents").insert({
        "user_id": user_info["user_id"],
        "filename": file.filename,
        "file_size": file_size,
        "file_type": file_type,
        "storage_path": f"{user_info['user_id']}/{file.filename}",
        "status": "uploaded"
    }).execute()

    document_id = doc_result.data[0]["id"]

    # Upload to Supabase Storage
    storage_path = f"{user_info['user_id']}/{document_id}/{file.filename}"

    try:
        supabase.storage.from_("documents").upload(storage_path, file_bytes)
    except Exception as e:
        # If upload fails, update document status to failed
        supabase.table("documents").update({
            "status": "failed",
            "error_message": f"Storage upload failed: {str(e)}"
        }).eq("id", document_id).execute()
        raise HTTPException(500, f"Failed to upload file to storage: {str(e)}")

    # Update storage_path
    supabase.table("documents").update({
        "storage_path": storage_path
    }).eq("id", document_id).execute()

    # Start background processing
    asyncio.create_task(process_document(document_id, user_info["user_id"]))

    return {"id": document_id, "status": "uploaded", "filename": file.filename}

@router.get("")
async def list_documents(user_info: dict = Depends(verify_token)):
    """List user's documents."""
    supabase = get_supabase_client_with_token(user_info["token"])
    result = supabase.table("documents")\
        .select("*")\
        .eq("user_id", user_info["user_id"])\
        .order("created_at", desc=True)\
        .execute()
    return result.data

@router.get("/{document_id}")
async def get_document(document_id: str, user_info: dict = Depends(verify_token)):
    """Get document details."""
    supabase = get_supabase_client_with_token(user_info["token"])
    result = supabase.table("documents")\
        .select("*")\
        .eq("id", document_id)\
        .eq("user_id", user_info["user_id"])\
        .single()\
        .execute()

    if not result.data:
        raise HTTPException(404, "Document not found")

    return result.data

@router.delete("/{document_id}")
async def delete_document(document_id: str, user_info: dict = Depends(verify_token)):
    """Delete document and all its chunks."""
    supabase = get_supabase_client_with_token(user_info["token"])

    # Verify ownership and get storage path
    doc = supabase.table("documents")\
        .select("storage_path")\
        .eq("id", document_id)\
        .eq("user_id", user_info["user_id"])\
        .single()\
        .execute()

    if not doc.data:
        raise HTTPException(404, "Document not found")

    # Delete from storage
    try:
        supabase.storage.from_("documents").remove([doc.data["storage_path"]])
    except Exception as e:
        # Log error but continue with database deletion
        print(f"Warning: Failed to delete file from storage: {e}")

    # Delete from database (chunks cascade delete)
    supabase.table("documents").delete().eq("id", document_id).execute()

    return {"status": "deleted"}
