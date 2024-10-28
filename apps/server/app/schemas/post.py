from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .user import UserResponse

class PostBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    published: Optional[bool] = False
    tags: List[str] = []

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None

class PostInDB(PostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PostResponse(PostBase):
    id: str
    author: UserResponse
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
