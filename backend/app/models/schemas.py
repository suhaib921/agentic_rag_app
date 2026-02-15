from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ThreadCreate(BaseModel):
    title: Optional[str] = None

class ThreadResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

class MessageResponse(BaseModel):
    id: str
    thread_id: str
    user_id: str
    role: str
    content: str
    created_at: datetime
