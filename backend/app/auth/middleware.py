from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import create_client, Client
from app.config import settings

security = HTTPBearer()
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Verify Supabase JWT and return user info."""
    try:
        token = credentials.credentials
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {
            "user_id": response.user.id,
            "email": response.user.email,
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Auth failed: {str(e)}")
