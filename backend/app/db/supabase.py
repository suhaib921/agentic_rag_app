from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

def get_supabase_client() -> Client:
    """Create Supabase client with service role key for background processing.

    This client bypasses RLS and should only be used for server-side operations
    like document ingestion that don't involve user authentication.
    """
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )
